"""
从大模型的回答中提取信息
"""
import re
import json


def nodes_text_to_list_of_dict(nodes: str) -> list[dict]:
    regex = r"\[(.*?)\]"
    jsonRegex = r"\{.*\}"
    result = []
    matches = re.findall(regex, nodes, re.MULTILINE)

    for match in matches:
        raw_node = str(match).strip().split(",")
        if len(raw_node) < 2:
            continue
        name = raw_node[0].replace('"', "").strip()
        label = raw_node[1].replace('"', "").strip()
        properties = re.search(jsonRegex, match)
        if properties is None:
            properties = None
        else:
            properties = properties.group(0)
        properties = properties.replace("True", "true")
        properties = properties.replace("False", "false")
        try:
            properties = json.loads(properties)
        except:
            properties = {}
        result.append({"name": name, "label": label, "properties": properties})

    return result


def relationships_text_to_list_of_dict(relations: str) -> list[dict]:
    regex = r"\[(.*?)\]"
    jsonRegex = r"\{.*\}"

    result = []
    matches = re.findall(regex, relations, re.MULTILINE)

    for match in matches:
        raw_relationship = str(match).strip().split(",")
        if len(raw_relationship) < 3:
            continue

        start = raw_relationship[0].replace('"', "").strip()
        relationship_type = raw_relationship[1].replace('"', "").strip()
        end = raw_relationship[2].replace('"', "").strip()

        properties = re.search(jsonRegex, match)
        if properties is None:
            properties = None
        else:
            properties = (
                properties.group(0)
                .strip()
                .replace("True", "true")
                .replace("False", "false")
            )
        try:
            properties = json.loads(properties)
        except:
            properties = {}

        result.append(
            {
                "start": start,
                "end": end,
                "type": relationship_type,
                "properties": properties,
            }
        )
    return result


def get_nodes_relationships_from_rawtext(rawtext: str) -> dict:
    regex = r"Nodes:\s*([\s\S]*?)Relationships:\s*([\s\S]*)"

    result = dict()
    matches = re.findall(regex, rawtext, re.DOTALL)

    raw_nodes = ""
    raw_relationships = ""

    for matchNum, match in enumerate(matches, start=1):
        if len(match) > 1:
            raw_nodes = match[0]
            raw_relationships = match[1]
        break

    result["nodes"] = []
    result["relationships"] = []

    result["nodes"].extend(nodes_text_to_list_of_dict(raw_nodes))
    result["relationships"].extend(
        relationships_text_to_list_of_dict(raw_relationships)
    )

    return result


def duplicate_nodes_relationships(data: dict[str, list]) -> dict:
    # 创建一个字典来存储合并后的节点和关系
    merged_nodes = {}
    merged_relationships = {}

    # 合并节点
    for node in data["nodes"]:
        key = (node["name"], node["label"])
        if key not in merged_nodes:
            merged_nodes[key] = node
        else:
            merged_nodes[key]["properties"].update(node["properties"])

    node_names = [node["name"] for node in list(merged_nodes.values())]

    # 合并关系
    for relationship in data["relationships"]:
        key = (relationship["start"], relationship["type"], relationship["end"])
        if key not in merged_relationships:
            start_key = relationship.get("start", None)
            end_key = relationship.get("end", None)
            if (start_key in node_names) and (end_key in node_names):
                merged_relationships[key] = relationship
        else:
            merged_relationships[key]["properties"].update(relationship["properties"])

    # 将合并后的节点和关系转换回列表
    data["nodes"] = list(merged_nodes.values())
    data["relationships"] = list(merged_relationships.values())

    return data


def extract_cypher_from_rawtext(rawtext: str) -> str:
    pattern = re.compile(r"```cypher(.*?)```", re.DOTALL)
    matches = pattern.findall(rawtext)
    scripts = [match.strip() for match in matches]
    # 连接所有脚本，每两个脚本之间以一个空行分隔
    combined_script = "\n\n".join(scripts)
    return combined_script


def text_splitter_txt_zh(text: str, chunk_size: int, overlap: int) -> list[str]:
    """中文纯文本切割"""
    chunks = []
    index = 0
    while index < len(text):
        if index + chunk_size >= len(text):
            chunks.append(text[index + 1:])
            break
        end_index = index + chunk_size
        if end_index < len(text):
            while end_index > index and text[end_index] not in "。？！；\n":
                end_index -= 1
        if end_index == index:
            end_index = index + chunk_size
        chunks.append(text[index + 1: end_index + 1])
        overlap_index = end_index - overlap
        if overlap_index > index:
            while overlap_index > index and text[overlap_index] not in "。？！\n":
                overlap_index -= 1
            if overlap_index == index:
                overlap_index = end_index - overlap
        index = overlap_index
    return chunks
