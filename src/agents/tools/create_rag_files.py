import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import dotenv
from tqdm import tqdm
import logging

# Load environment variables
dotenv.load_dotenv("../../../.env")

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')


class ReadWebPage:
    def __init__(self):
        pass

    def is_valid_url(self, url: str):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    async def run(self, url: str, original_text: str) -> str:
        valid_url = self.is_valid_url(url)
        if not valid_url:
            return "Invalid URL. Please enter a valid URL."

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as res:
                    if res.status != 200:
                        return "Error fetching web page. Please try again."
                    text = await res.text()
                    soup = BeautifulSoup(text, "html.parser")
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
            except Exception as e:
                logging.error(f"Error fetching URL {url}: {str(e)}")
                return "Error occurred while fetching the web page."


async def main():
    r = ReadWebPage()

    base_url = "https://en.wikipedia.org"
    rag_url = "https://fastgpt.wenzhaoabc.com/api/core/dataset/collection/create/text"

    urls = []
    with open("../../test/ulrs.txt", "r", encoding="utf-8") as f:
        for line in f:
            urls.append(line.strip())

    body = {
        "datasetId": "6649852eff0a4fb917024cbe",
        "trainingType": "chunk",
        "chunkSize": 2000,
        "chunkSplitter": "",
        "metadata": {}
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('RAG_API_KEY')}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        for i, u in enumerate(tqdm(urls, desc="Processing URLs", unit="url")):
            try:
                text = await r.run(base_url + u, "")
            except Exception as e:
                error_message = f"Request to {u} error, reason: {str(e)}"
                print(error_message)
                logging.error(error_message)
                continue
            body["text"] = text
            body["name"] = u.split("/")[-1]
            try:
                async with session.post(rag_url, headers=headers, json=body) as res:
                    print(await res.text())
            except Exception as e:
                error_message = f"Error posting data for {u}, reason: {str(e)}"
                print(error_message)
                logging.error(error_message)


# Run the main function
asyncio.run(main())
