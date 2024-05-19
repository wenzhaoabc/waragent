"""
使用RAG的方式检索相关内容
"""
import os
from openai import OpenAI


class RAG:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("RAG_BASE_URL"),
            api_key=os.getenv("RAG_API_KEY"),
        )

    def retrival(self, question: str) -> str:
        res = self.client.chat.completions.create(
            model="WarAgent",
            messages=[{"role": "user", "content": question}],
            stream=False
        )
        return res.choices[0].message.content


# import dotenv
# dotenv.load_dotenv("../../.env")
#
# rag = RAG()
# p = rag.retrival("Hello!")
# print(p)
