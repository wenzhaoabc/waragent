import os
import re

from src.llm import LLM

from .neo4j_db import Neo4JDB
from .summary_results import SummarizeCypherResult
from .query_prompts import (p_get_fewshot_examples, p_generate_cypher_prompt)


class Neo4jAnswers:
    def __init__(self, llm: LLM = None):
        if llm is None:
            llm = LLM()
        self.llm = llm
        self.db = Neo4JDB()
        self.summarize = SummarizeCypherResult(llm, exclude_embeddings=False)

    def p_system_prompt(self, database_schema: str) -> str:
        return (
            f"{p_generate_cypher_prompt()}\n\n"
            "The following is the schema of the database:\n\n"
            f"{database_schema}\n"
            "Here is some examples of how to do this work:\n"
            f"{p_get_fewshot_examples(os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_BASE_URL"))}\n\n"
            "Please note that, your output should follow the following format:\n"
            "```cypher\n"
            "<your cypher query>"
            "```"
        )

    def p_try_again_prompt(self, origin_res: str, exception: str) -> str:
        return (
            f"You just generate one cypher query, but occur an exception:{exception}. Please try again!"
            f"Your origin cypher query is: ```cypher\n{origin_res}\n```."
        )

    def generate_cypher(self, messages: list[dict[str, str]]) -> str:
        llm_res = self.llm.generate(messages)
        res_regex = r"```cypher(.*?)```"
        res = re.findall(res_regex, llm_res, re.DOTALL)
        cypher = [item.strip() for item in res][0]
        return cypher

    def neo4j_answers(self, question: str) -> str:
        neo4j_schema = self.db.get_schema()
        system_prompt = self.p_system_prompt(neo4j_schema)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]
        cypher = self.generate_cypher(messages)
        try:
            query_result = self.db.query(cypher)
        except Exception as e:
            messages.append({"role": "user", "content": self.p_try_again_prompt(cypher, str(e))})
            cypher = self.generate_cypher(messages)
            try:
                query_result = self.db.query(cypher)
            except Exception as e:
                return "There are no useful information in the database about this question."

        answers = self.summarize.run(question, query_result)
        return answers
