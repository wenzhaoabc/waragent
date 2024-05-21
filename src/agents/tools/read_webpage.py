import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class ReadWebPage:
    definition = {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": "Extract text information from web pages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Extract the address of the page information.",
                    },
                    "original_text": {
                        "type": "string",
                        "description": "The original text of the search request.",
                    },
                },
                "required": ["url", "original_text"],
            },
        },
    }

    def __init__(self):
        pass

    def is_valid_url(self, url: str):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def run(self, url: str, original_text: str) -> str:
        valid_url = self.is_valid_url(url)
        if not valid_url:
            return "Invalid URL. Please enter a valid URL."
        proxies = {"http": os.getenv("HTTP_PROXY"), "https": os.getenv("HTTPS_PROXY")}
        res = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            },
            proxies=proxies,
        )
        if res.status_code != 200:
            return "There no content in this URL."
        soup = BeautifulSoup(res.text, "html.parser")
        if soup is None:
            return "There no content in this URL."
        # 获取网页的标题
        title = soup.title.string
        # 获取网页的正文
        soup = soup.find("body")
        for tag in soup(["script", "style"]):
            tag.decompose()
        for tag in soup(["img", "link", "source"]):
            tag.decompose()
        for tag in soup.find_all(["a", "span", "bold", "pre"]):
            tag.unwrap()
        for tag in soup.find_all(True):
            tag.attrs = {}

        return f"WebPage Title:{title}\n\n" + str(soup)
