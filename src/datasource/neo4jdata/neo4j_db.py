import os
import re

from neo4j import GraphDatabase
from .cypher_snippets import nodes_cypher, relationships_cypher

node_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
RETURN {labels: nodeLabels, properties: properties} AS output
"""

rel_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
RETURN {type: nodeLabels, properties: properties} AS output
"""

rel_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE type = "RELATIONSHIP" AND elementType = "node"
RETURN "(:" + label + ")-[:" + property + "]->(:" + toString(other[0]) + ")" AS output
"""


def schema_text(node_props, rel_props, rels) -> str:
    return f"""
  This is the schema representation of the Neo4j database.
  Node properties are the following:
  {node_props}
  Relationship properties are the following:
  {rel_props}
  The relationships are the following
  {rels}
  """


class Neo4JDB:
    def __init__(self, uri: str = None, username: str = None, password: str = None) -> None:
        uri = uri if uri is not None else os.environ.get("NEO4J_URI")
        username = username if username is not None else os.environ.get("NEO4J_USER")
        password = password if password is not None else os.environ.get("NEO4J_PASSWD")
        self.uri = uri
        self.auth = (username, password)
        self.schema = ""

    def load_cypher(self, cypher: str) -> dict:
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            records, summary, keys = driver.execute_query(cypher)
        res = {"records": [r.data() for r in records], "keys": keys}
        return res

    def query(self, cypher: str, params: dict | None = None) -> list:
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            result, _, _ = driver.execute_query(cypher, parameters_=params)
        return [r.data() for r in result]

    def get_schema(self):
        with GraphDatabase.driver(self.uri, auth=self.auth):
            node_props = [el["output"] for el in self.query(node_properties_query)]
            rel_props = [el["output"] for el in self.query(rel_properties_query)]
            rels = [el["output"] for el in self.query(rel_query)]
            schema = schema_text(node_props, rel_props, rels)
            self.schema = schema
            return schema

    def check_if_empty(self) -> bool:
        data = self.query(
            """
        MATCH (n)
        WITH count(n) as c
        RETURN CASE WHEN c > 0 THEN true ELSE false END AS output
        """
        )
        return data[0]["output"]

    def clean_db(self):
        self.load_cypher(
            """
            MATCH (n) DETACH DELETE n
            """
        )

    def import_json(self, file_url: str):
        nodes_script = re.sub(r'(?<=apoc.load.json\(").+?(?="\))', file_url, nodes_cypher)
        relations_script = re.sub(r'(?<=apoc.load.json\(").+?(?="\))', file_url, relationships_cypher)
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            record_n = driver.execute_query(nodes_script)
            print("node", record_n)
            nodes_count = record_n[0][0][0]
            record_r = driver.execute_query(relations_script)
            print("relationship", record_r)
            relation_count = record_r[0][0][0]
            return {"nodes_count": nodes_count, "relationship_count": relation_count}
