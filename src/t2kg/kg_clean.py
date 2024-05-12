import json

from itertools import groupby

from src.llm import LLM

from .text_extract import nodes_text_to_list_of_dict, relationships_text_to_list_of_dict


def generate_system_message_for_nodes() -> str:
    return """Your task is to identify if there are duplicated nodes and if so merge them into one nod. Only merge the nodes that refer to the same entity.
You will be given different datasets of nodes and some of these nodes may be duplicated or refer to the same entity. 
The datasets contains nodes in the form [ENTITY_ID, TYPE, PROPERTIES]. When you have completed your task please give me the 
resulting nodes in the same format. Only return the nodes and relationships no other text. If there is no duplicated nodes return the original nodes.

Here is an example of the input you will be given:
["alice", "Person", {"age": 25, "occupation": "lawyer", "name":"Alice"}], ["bob", "Person", {"occupation": "journalist", "name": "Bob"}], ["alice.com", "Webpage", {"url": "www.alice.com"}], ["bob.com", "Webpage", {"url": "www.bob.com"}]
"""


def generate_system_message_for_relationships() -> str:
    return """
Your task is to identify if a set of relationships make sense.
If they do not make sense please remove them from the dataset.
Some relationships may be duplicated or refer to the same entity. 
Please merge relationships that refer to the same entity.
The datasets contains relationships in the form [ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES].
You will also be given a set of ENTITY_IDs that are valid.
Some relationships may use ENTITY_IDs that are not in the valid set but refer to a entity in the valid set.
If a relationships refer to a ENTITY_ID in the valid set please change the ID so it matches the valid ID.
When you have completed your task please give me the valid relationships in the same format. Only return the relationships no other text.

Here is an example of the input you will be given:
["alice", "roommate", "bob", {"start": 2021}], ["alice", "owns", "alice.com", {}], ["bob", "owns", "bob.com", {}]
"""


def generate_prompt(data) -> str:
    return f""" Here is the data:
{data}
"""


class DataDisambiguation:
    def __init__(self, llm: LLM):
        self.llm = llm

    def disambiguate(self, kg: dict[str, list[dict]]) -> dict[str, list[dict]]:
        """
        node: [{name,label,properties}]
        relationship: [{start,end,type,properties}]
        """
        nodes = sorted(kg["nodes"], key=lambda x: x["label"])
        relationships = sorted(kg["relationships"], key=lambda x: x["start"])

        new_nodes = []
        new_relationships = []

        node_groups = groupby(nodes, key=lambda x: x["label"])
        for group in node_groups:
            dis_string = ""
            nodes_in_group = list(group[1])
            if len(nodes_in_group) == 1:
                new_nodes.extend(nodes_in_group)
                continue

            for node in nodes_in_group:
                dis_string += (
                        '["'
                        + node["name"]
                        + '", "'
                        + node["label"]
                        + '", '
                        + json.dumps(node["properties"])
                        + "]\n"
                )

            message = [
                {"role": "system", "content": generate_system_message_for_nodes()},
                {"role": "user", "content": generate_prompt(dis_string)}
            ]
            raw_node_text = self.llm.generate(messages=message)
            new_nodes.extend(nodes_text_to_list_of_dict(raw_node_text))

        relationship_data = "Relationships:\n"
        for relation in relationships:
            relationship_data += (
                    '["'
                    + relation["start"]
                    + '", "'
                    + relation["type"]
                    + '", "'
                    + relation["end"]
                    + '", '
                    + json.dumps(relation["properties"])
                    + "]\n"
            )
        node_labels = [node["name"] for node in new_nodes]
        relationship_data += "Valid Nodes:\n" + "\n".join(node_labels)
        message = [
            {"role": "system", "content": generate_system_message_for_relationships()},
            {"role": "user", "content": generate_prompt(relationship_data)}
        ]
        raw_relation_text = self.llm.generate(messages=message)
        new_relationships.extend(relationships_text_to_list_of_dict(raw_relation_text))

        return {"nodes": new_nodes, "relationships": new_relationships}
