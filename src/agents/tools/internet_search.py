"""
工具调用，Google搜索
"""
import os
import requests


class InternetSearch:
    definition = {
        "type": "function",
        "function": {
            "name": "google_search",
            "description": "Use Google to search for keywords. Each search will return 10 search results (sorted by relevance, each result contains a website, webpage description[snippet], ranking[position], etc.). You can use the ReadWebpage Action to further access these webpages, and a knowledge graph (if available).",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Keywords used to search on Google",
                    },
                    "locale": {
                        "type": "string",
                        "description": "Google uses this parameter to customize the language in the search location, following the ISO-639 standard. For example, entering `en` will search for English language web pages. The default is `en`.",
                        "enum": ["en", "zh", "jp", "de", "fr"],
                    },
                    "country": {
                        "type": "string",
                        "description": "Google uses this parameter to customize the country information in the search location, using a two-letter lowercase country code. For example, entering `us` will prioritize searching web pages in the United States region.The default is `us`.",
                    },
                    "original_text": {
                        "type": "string",
                        "description": "The original text of the search request.",
                    }
                },
                "required": ["keywords", "original_text"],
            },
        },
    }

    def __init__(self):
        pass

    def run(self, keywords: str, original_text: str, locale: str = 'en', country: str = 'us') -> list[dict]:
        headers = {"Authorization": "Bearer " + os.getenv("TOOLS_TOKEN")}
        url = os.getenv("TOOLS_URL") + "/api/v1/searchgoogle"
        req_body = {
            "keywords": keywords,
            "original_text": original_text,
            "locale": locale,
            "country": country,
        }
        response = requests.post(url, headers=headers, json=req_body)
        if response.status_code != 200:
            c = response.content
            return []
        res = response.json()
        if "organic" in res["data"]:
            return res["data"]["organic"]
