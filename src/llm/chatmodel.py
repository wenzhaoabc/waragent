import os
from openai import OpenAI

from src.utils import log


class LLM(object):
    def __init__(self,
                 model: str = "gpt-4",
                 base_url: str = os.getenv("OPENAI_BASEURL"),
                 api_key: str = os.getenv("OPENAI_API_KEY"),
                 temperature: float = 0.2,
                 ):
        self.model = model
        self.temperature = temperature
        if base_url is None or api_key is None:
            log.error("Base URL or API KEY must be set")
            raise ValueError("Base URL or API KEY is None")
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

    def chat_v(self, prompt: str, img_url: str, callback: callable = None, temperature: float = 0.2):
        if self.model != "gpt-4-turbo":
            raise ValueError(f"mode {self.model} doesn't support visual model")
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": img_url}, }
                    ],
                }
            ],
            stream=True,
            max_tokens=300,
        )
        res = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                if callback is not None:
                    callback(content)
                res += content

        log.info(f"chat with [{self.model}]: messages:{prompt} ;image:{img_url} response:{res}")
        return res
