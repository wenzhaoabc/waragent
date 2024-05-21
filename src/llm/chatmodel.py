import json
import os
from datetime import datetime

from openai import OpenAI
from zhipuai import ZhipuAI

from src.utils import log


class LLM(object):
    def __init__(
            self,
            model: str = "qwen-plus",
            base_url: str = os.getenv("OPENAI_BASE_URL"),
            api_key: str = os.getenv("OPENAI_API_KEY"),
            temperature: float = 0.2,
            system_prompt: str = None,
    ):
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt
        if base_url is None or api_key is None:
            log.error("Base URL or API KEY must be set")
            raise ValueError("Base URL or API KEY is None")
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        if model.startswith("glm"):
            api_key = os.getenv("ZHIPU_API_KEY")
            base_url = os.getenv("ZHIPU_BASE_URL")
            self.client = ZhipuAI(api_key=api_key, base_url=base_url)

    def chat(self, prompt: str, temperature: float = 0.2):
        timestamp = datetime.now().timestamp()
        log.info(
            f'chat with {self.model} : {json.dumps({"id": timestamp, "model": self.model, "prompt": prompt, "temperature": temperature})}'
        )
        completions = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=temperature or self.temperature,
        )
        response = completions.choices[0].message.content
        log.info(
            f'chat with [{self.model}]: {{"id":{timestamp},"message":{{"role": "user", "content": {prompt}}}, "response": {completions.model_dump_json()}}}'
        )
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
        timestamp = datetime.now().timestamp()
        log.info(
            f'chat to {self.model} : {{"id": {timestamp}, "messages": {json.dumps(messages)}}}"}}'
        )
        completes = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.1
        )
        response = completes.choices[0].message.content
        log.info(
            f'chat with [{self.model}]: {{"id": {timestamp},"messages":{json.dumps(messages)},"response":{completes.model_dump_json()} }}'
        )
        return response

    def generate_stream(
            self, messages: list[dict[str, str]], callback: callable
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, stream=True
        )
        res = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                if callback is not None:
                    callback(content)
                res += content

        log.info(f"chat with [{self.model}]: messages:{messages} response:{res}")
        return res

    def chat_v(
            self,
            prompt: str,
            img_url: str,
            callback: callable = None,
            temperature: float = 0.2,
    ):
        if self.model != "gpt-4-turbo":
            raise ValueError(f"mode {self.model} doesn't support visual model")
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": img_url},
                        },
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

        log.info(
            f"chat with [{self.model}]: messages:{prompt} ;image:{img_url} response:{res}"
        )
        return res

    def chat_with_tools(
            self, messages: list[dict[str, str]], tools: list, tool_choices: str = "auto"
    ):
        timestamp = datetime.now().timestamp()
        log.info(
            f"chat with [{self.model}] with function call : {json.dumps({"id": timestamp, "messages": messages, "tools": tools, "tool_choices": tool_choices})}"
        )
        res = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
            temperature=self.temperature,
            tools=tools,
            tool_choice=tool_choices,
        )
        # res = res.model_dump_json()
        log.info(
            f'chat with [{self.model}]: {{"id":{timestamp},"messages":{json.dumps(messages)}, "tools":{tools}, "tool_choices":{tool_choices}, "response":{res.model_dump_json()} }}')
        return res.choices[0]

    def max_tokens(self, model_name: str) -> int:
        model_max_tokens = {
            "gpt-4o": 128000,
            "glm-4": 128000,
            "gpt-4-turbo": 128000,
            "gpt-4": 8192,
            "gpt-3.5-turbo-0125": 16385,
            "qwen-plus": 30000,
            "qwen-max": 6000,
        }
        return model_max_tokens[model_name]
