import pandas as pd
import requests
import tqdm

from ..scraping import (
    get_page,
    get_text_from_xpath_list,
    get_preview_url_from_xpath_list,
    get_href_from_xpath_list
)

def get_all_genres() -> pd.DataFrame:
    """Get all genres from everynoise.com"""
    url = "https://everynoise.com/engenremap.html"
    page = get_page(url)
    genres = get_text_from_xpath_list(page, ".//div[@class='canvas']/div")
    preview_urls = get_preview_url_from_xpath_list(page, ".//div[@class='canvas']/div")
    hrefs = get_href_from_xpath_list(page, ".//div[@class='canvas']/div/a")
    return pd.DataFrame({"genre": genres, "preview_url": preview_urls, "href": hrefs})

def get_all_musics_from_genre(genre: str) -> pd.DataFrame:
    """Get all musics from a genre"""
    url = f"https://everynoise.com/{genre}"
    page = get_page(url)
    musics = get_text_from_xpath_list(page, ".//div[@class='canvas']/div")
    preview_urls = get_preview_url_from_xpath_list(page, ".//div[@class='canvas']/div")
    return pd.DataFrame({"music": musics, "preview_url": preview_urls})

def download_preview_songs(df: pd.DataFrame, genre: str) -> None:
    """Download preview songs from a genre"""
    for artist, preview_url in tqdm.tqdm(zip(df["music"], df["preview_url"]), total=len(df)):
        response = requests.get(preview_url)
        if response.status_code == 200:
            with open(f"../data/genres/{genre}/{artist}.wav", "wb") as f:
                f.write(requests.get(preview_url).content)
        else:
            print(f"Error downloading {artist}")