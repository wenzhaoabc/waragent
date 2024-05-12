"""
知识图谱转为导入到Neo4j的cypher脚本
"""
import random
import re

from src.llm import LLM

from .kg_prompts import to_cypher_system_prompt, to_cypher_user_prompt

default_cypher = """
CALL apoc.load.json("file:///path/to/json") YIELD value AS data
UNWIND data.nodes AS node
CALL apoc.merge.node([node.label], {name: node.name}, node.properties) YIELD node as n
WITH data, n
UNWIND  data.relationships AS rel
MATCH (start {name: rel.start}), (end {name: rel.end})
CALL apoc.create.relationship(start, rel.type, rel.properties, end) YIELD rel as r 
RETURN n, r
"""

nodes_cypher = """
CALL apoc.load.json("https://text2img.oss-cn-shanghai.aliyuncs.com/retrival/20240410154312_origin.json") YIELD value AS data
UNWIND data.nodes AS node
CALL apoc.merge.node([node.label], {name: node.name}, node.properties) YIELD node as n
RETURN count(n) AS nodesCreated
"""

relations_cypher = """
CALL apoc.load.json("https://text2img.oss-cn-shanghai.aliyuncs.com/retrival/20240410154312_origin.json") YIELD value AS data
UNWIND data.relationships AS rel
MATCH (head {name: rel.start})
MATCH (tail {name: rel.end})
CALL apoc.create.relationship(head, rel.type, rel.properties, tail) YIELD rel as r
RETURN count(r) AS relationshipsCreated
"""


class KG2Cypher(object):
    def __init__(
            self,
            llm: LLM,
            file_url: str,
            schema: str = None,
    ) -> None:
        self.llm = llm
        self.file_url = file_url
        self.schema = schema

    def request_to_ai(self, content: str) -> str:
        messages = [
            {"role": "system", "content": to_cypher_system_prompt()},
            {"role": "user", "content": to_cypher_user_prompt(content=content)},
        ]
        raw_res = self.llm.generate_stream(messages=messages, callback=None)
        return raw_res

    def process(self, kgs: dict[str, list]) -> dict[str, str]:
        example = dict[str, list]()
        example["nodes"] = random.sample(kgs["nodes"], len(kgs["nodes"]))
        example["relationships"] = random.sample(
            kgs["relationships"], len(kgs["relationships"])
        )
        # TODO Request to LLM to get cypher
        new_path = self.file_url
        nodes_script = re.sub(r'(?<=apoc.load.json\(").+?(?="\))', new_path, nodes_cypher)
        relations_script = re.sub(r'(?<=apoc.load.json\(").+?(?="\))', new_path, relations_cypher)
        return {"nodes": nodes_script, "relationships": relations_script}
