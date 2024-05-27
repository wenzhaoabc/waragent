from .enums import LanguageEnum


def to_kg_system_prompt(
        language: LanguageEnum = LanguageEnum.zh, example: str = None
) -> str:
    if example is None:
        if language == LanguageEnum.en:
            example = """
Data: The German Panzer IV tank was widely used during World War II. It was introduced in 1939 and played a crucial role in the German military strategy. The United States developed the M4 Sherman tank, which was introduced in 1942 and became the primary tank used by the Allies. Both tanks were critical in various battles, including the Battle of Normandy in 1944.
Nodes: 
- ["Panzer IV", "Tank", {"country": "Germany", "introduction_year": 1939, "role": "German military strategy"}]
- ["M4 Sherman", "Tank", {"country": "United States", "introduction_year": 1942, "role": "primary tank for Allies"}]
- ["World War II", "Event", {"start_year": 1939, "end_year": 1945}]
- ["Battle of Normandy", "Battle", {"year": 1944}]
Relationships: 
- ["Panzer IV", "used_in", "World War II", {}]
- ["M4 Sherman", "used_in", "World War II", {}]
- ["Panzer IV", "participated_in", "Battle of Normandy", {}]
- ["M4 Sherman", "participated_in", "Battle of Normandy", {}]
- ["World War II", "includes", "Battle of Normandy", {}]
"""
        elif language == LanguageEnum.zh:
            example = """
文本数据:李薇是律师，今年25岁，Bob从2001年起就是她的室友。Bob是一名记者。李薇拥有网页www.liwei.com, Bob拥有网页www.bob.com。
Nodes:
- ["李薇", "人", {"年龄":25, "职业":"律师"、"姓名":"李薇"}]
- ["Bob", "人", {"职业":"记者","姓名":"Bob"}]
- ["liwei.com", "网站", {"网址": "www.liwei.com"}]
- ["bob.com", "网站", {"网址": "www.bob.com"}]
Relationships:
- ["李薇", "室友", "Bob", {"开始时间":2021}]
- ["李薇", "拥有", "liwei.com", {}]
- ["Bob", "拥有", "bob.com", {}]
"""
    if language == LanguageEnum.en:
        return f"""
You are a data scientist working for a company that is building a graph database. Your task is to extract information from data and convert it into a graph database.
Provide a set of Nodes in the form [ENTITY_ID, TYPE, PROPERTIES] and a set of relationships in the form [ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES].
It is important that the ENTITY_ID_1 and ENTITY_ID_2 exists as nodes with a matching ENTITY_ID. If you can't pair a relationship with a pair of nodes don't add it.
When you find a node or relationship you want to add try to create a generic TYPE for it that  describes the entity you can also think of it as a label.

Example:
{example}
"""
    elif language == LanguageEnum.zh:
        return f"""
你是一名数据科学家，在一家正在构建图形数据库的公司工作。您的任务是从文本数据中提取信息并将其转换为图形数据库中适用的格式。
请以[ENTITY_ID, TYPE, PROPERTIES]的形式提取一组节点，并以[ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES]的形式提取一组关系。
需要注意，ENTITY_ID_1和ENTITY_ID_2应当具有匹配ENTITY_ID的节点存在。如果你不能将一个关系与一对节点配对，那就不要添加它。
当您找到想要添加的节点或关系时，请尝试为其创建描述实体的抽象TYPE，您也可以将其视为标签。请直接输出您提取出的节点和关系，不要输出任何分析过程。

例子:
{example}
"""
    else:
        return ""


def to_kg_user_prompt(content: str, language: LanguageEnum) -> str:
    if language == LanguageEnum.zh:
        return f"""
文本数据: {content}
"""
    elif language == LanguageEnum.en:
        return f"""
Data: {content}
        """


def to_cypher_system_prompt(example: str = None) -> str:
    return """
你现在是一个neo4j图数据库开发专家，现在需要你将json数据通过neo4j的拓展库apoc.load.json()将json文件加载到neo4j数据库中。
请给出完整的Cypher脚本，将脚本包裹在```cypher <cypher脚本>```内，不需要给出分析过程。
json数据中包含nodes和relationships。
node的结构为{name:"<name value>","label":"<label value>","properties":{"k1":"v1",{"k2":"v2"},...}}
relationship的结构为{"start":"<start node name>","end":"<end node name>","type":"<relationship type value>","properties":{"k1":"v1",{"k2":"v2"},...}}
"""


def to_cypher_user_prompt(content: str) -> str:
    return f"""
示例JSON数据：
```json
{content}
```
"""
