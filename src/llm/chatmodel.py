import os
from openai import OpenAI

from src.utils import log


class LLM(object):
    def __init__(self,
                 model: str = "gpt-4",
                 base_url: str = os.getenv("BASE_URL") or "https://api.llm.wenzhaoabc.com/v1",
                 api_key: str = os.getenv("API_KEY") or "sk-1234",
                 temperature: float = 0.2,
                 ):
        self.model = model
        self.temperature = temperature
        if base_url is None or api_key is None:
            log.error("Base URL or API_KEY must be set")
            raise ValueError("Base URL or API_KEY is None")
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, prompt: str, temperature: float = 0.2):
        completions = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=temperature or self.temperature,
        )
        response = completions.choices[0].message.content
        log.info(f"chat with [{self.model}]: prompt:{prompt} response:{response}")
        return response

    def chat_stream(self, prompt: str, callback: callable, temperature: float = 0.2):
        completions = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
            temperature=temperature or self.temperature,
        )
        result = ""
        for chunk in completions:
            if chunk.choices[0].delta.content is not None:
                callback(chunk.choices[0].delta.content)
                result += chunk.choices[0].delta.content
        log.info(f"chat with [{self.model}]: prompt:{prompt} response:{result}")
        return result

    def generate(self, messages: list[dict[str, str]]) -> str:
        completes = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )

        response = completes.choices[0].message.content
        log.info(f"chat with [{self.model}]: messages:{messages} response:{response}")
        return response

    def generate_stream(self, messages: list[dict[str, str]], callback: callable) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        res = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                callback(content)
                res += content

        log.info(f"chat with [{self.model}]: messages:{messages} response:{res}")
        return res
