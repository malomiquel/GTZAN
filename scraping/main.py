import pandas as pd

from utils.scraping import get_page, get_text_from_xpath_list, get_preview_url_from_xpath_list, get_href_from_xpath_list


url = "https://everynoise.com/engenremap.html"

page = get_page(url)

genres = get_text_from_xpath_list(page, ".//div[@class='canvas']/div")
print(len(genres))
preview_urls = get_preview_url_from_xpath_list(page, ".//div[@class='canvas']/div")
print(len(preview_urls))
hrefs = get_href_from_xpath_list(page, ".//div[@class='canvas']/div/a")
print(len(hrefs))