from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import requests
import re


def get_page(url: str) -> html.HtmlElement:
    """Get page from url"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    page = requests.get(url, headers=headers)
    return html.fromstring(page.content)


def get_page_with_selenium(url: str, class_name: str) -> html.HtmlElement:
    """Get page from url"""
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    )
    options.add_argument("window-size=1920x1080")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )

    html_content = driver.page_source
    with open("page.html", "w") as f:
        f.write(html_content)

    page = html.fromstring(html_content)
    return page


def parse_page(page: html.HtmlElement, xpath: str) -> html.HtmlElement:
    """Parse page with xpath"""
    return page.xpath(xpath)[0]


def parse_page_list(page: html.HtmlElement, xpath: str) -> list:
    """Parse page with xpath"""
    return page.xpath(xpath)


def get_text_from_xpath(page: html.HtmlElement, xpath: str) -> str:
    """Get text from xpath"""
    text = page.xpath(xpath + "/text()")
    if text:
        return clean_text(text[0])
    else:
        return None


def get_text_from_xpath_list(page: html.HtmlElement, xpath: str) -> list:
    """Get text from xpath"""
    return [clean_text(text) for text in page.xpath(xpath + "/text()") if text is not text.strip() != ""]


def get_href_from_xpath(page: html.HtmlElement, xpath: str) -> str:
    """Get href from xpath"""
    href = page.xpath(xpath + "/@href")
    if href:
        return href[0]
    else:
        return None


def get_href_from_xpath_list(page: html.HtmlElement, xpath: str) -> list:
    """Get href from xpath"""
    return page.xpath(xpath + "/@href")

def get_preview_url_from_xpath(page: html.HtmlElement, xpath: str) -> str:
    """Get preview url from xpath"""
    preview_url = page.xpath(xpath + "/@preview_url")
    if preview_url:
        return preview_url[0]
    else:
        return None
    
def get_preview_url_from_xpath_list(page: html.HtmlElement, xpath: str) -> list:
    """Get preview url from xpath"""
    return page.xpath(xpath + "/@preview_url")


def clean_text(text):
    """Clean text by removing specific characters and extra spaces."""
    text = re.sub(r"\|", "", text)  # Remove '|' characters
    text = re.sub(r"\n", "", text)  # Remove newline characters
    text = re.sub(r"\r", "", text)  # Remove carriage return characters
    text = re.sub(r"\t", "", text)  # Remove tab characters
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    return text.strip()
