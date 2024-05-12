"""
文本提取
"""
from src.utils import log
from src.llm import LLM

from .text_extract import (
    duplicate_nodes_relationships,
    get_nodes_relationships_from_rawtext,
    text_splitter_txt_zh
)
from .kg_prompts import to_kg_system_prompt, to_kg_user_prompt
from .enums import LanguageEnum


class ExtractKG:
    def __init__(self, llm: LLM, language: LanguageEnum, example: str = None):
        self.llm = llm
        self.language = language
        self.example = example

    def request_to_ai(self, content: str) -> str:
        messages = [
            {
                "role": "system",
                "content": to_kg_system_prompt(self.language, self.example),
            },
            {
                "role": "user",
                "content": to_kg_user_prompt(content, language=self.language),
            },
        ]
        log.info("request_to_ai messages: " + str(messages))
        # call_back = lambda c: print(c, end="")
        res = self.llm.generate_stream(messages, None)
        log.info("request_to_ai res: " + str(res))
        return res

    def get_token_num(self, content: str) -> int:
        if self.language == LanguageEnum.zh:
            return len(content) * 2
        else:
            # TODO compute content tokens
            return len(content) * 3 // 4

    def extract(self, content: str) -> dict[str, list]:
        allowed_tokens = (
                self.llm.max_tokens(self.llm.model)
                - self.get_token_num(to_kg_system_prompt(self.language))
                - self.get_token_num(to_kg_user_prompt("", language=self.language))
        )
        chunk_size = (
            allowed_tokens // 2
            if self.language == LanguageEnum.zh
            else allowed_tokens * 4
        )
        chunks = text_splitter_txt_zh(
            content, chunk_size, chunk_size // 10
        )

        results = dict[str, list]()
        results["nodes"] = []
        results["relationships"] = []
        for chunk in chunks:
            raw_text = self.request_to_ai(chunk)
            chunk_node_relationships = get_nodes_relationships_from_rawtext(raw_text)
            results["nodes"].extend(chunk_node_relationships["nodes"])
            results["relationships"].extend(chunk_node_relationships["relationships"])

        duplicated = duplicate_nodes_relationships(results)
        log.debug("duplicated_node_relationships" + str(duplicated))

        return duplicated
