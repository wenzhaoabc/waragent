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
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code != 200:
            return "Error fetching web page. Please try again."
        soup = BeautifulSoup(res.text, "html.parser")
        # 获取网页的标题
        title = soup.title.string
        # 获取网页的正文
        soup = soup.find("body")
        for tag in soup(["script", "style"]):
            tag.decompose()
        for tag in soup(["img", "link", "source"]):
            tag.decompose()
        for tag in soup.find_all(['a', 'span', 'bold', 'pre']):
            tag.unwrap()
        for tag in soup.find_all(True):
            tag.attrs = {}

        return f"WebPage Title:{title}\n\n" + str(soup)
