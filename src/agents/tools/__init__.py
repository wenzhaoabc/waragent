"""
工具调用模块
"""
from .read_webpage import ReadWebPage
from .internet_search import InternetSearch
from .anonymize import Anonymize
from .knowladeg_retrieval import KnowledgeRetrieval

AllTools = [
    {
        "type": "function",
        "function": {
            "name": "google_search",
            "description": "Use google to search for everything you want to know, including the economic and military situation of your own country and other countries. The tool returns the content of the web page that is most relevant to what you want to know, and you can summarize your answer based on the content of the web page.",
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
    },
    {
        "type": "function",
        "function": {
            "name": "knowledge_retrival",
            "description": "Search the war game knowledge base to get all the military and economic information about your country and other countries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Questions that require relevant answers from the knowledge base.",
                    },
                },
                "required": ["question"],
            },
        },
    }
]
