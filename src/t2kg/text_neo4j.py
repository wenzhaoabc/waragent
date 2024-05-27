"""

将文本抽取知识图谱导入到Neo4j中

"""

import json
import datetime

from src.datasource.neo4jdata.neo4j_db import Neo4JDB
from src.llm import LLM
from src.utils import upload_file_to_oss

from .extract_kgs import ExtractKG
from .enums import LanguageEnum
from .kg_clean import DataDisambiguation
from .kg_cypher import KG2Cypher


# step 1: 提取知识图谱 extract_kg
# step 2: 对知识图谱中的节点和关系进行清洗 clean_kg
# step 3: 将知识图谱上传到阿里云OSS text_neo4j/{timestamp_str}_kg.json
# step 4: 创建导入数据的cypher脚本 cypher
# step 5: 将知识图谱导入到图数据库Neo4j中 execute
# step 6: 返回结果 {"text": text, "kg": kg, "cypher": cypher, "execute_result": execute_results}
def extract_kgs_neo4j(
    text: str, neo4j: Neo4JDB, callback: callable, model: str = "qwen-max"
) -> dict:
    result = dict()
    result["text"] = text
    llm = LLM(model=model)
    # 提取知识图谱
    e = ExtractKG(llm=llm, language=LanguageEnum.en)
    kg = e.extract(text)
    callback({"type": "kg", "data": kg, "step": "extract_kg"})
    # 对知识图谱中的节点和关系进行清洗
    cleaner = DataDisambiguation(llm=llm)
    kg = cleaner.disambiguate(kg)
    result["kg"] = kg
    callback({"type": "kg", "data": kg, "step": "clean_kg"})

    # 将知识图谱上传到阿里云OSS
    timestamp_str = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    kg_filename = f"text_neo4j/{timestamp_str}_kg.json"
    file_oss_url = upload_file_to_oss(kg_filename, json.dumps(kg))

    execute_results = neo4j.import_json(file_oss_url)

    # 创建导入数据的cypher脚本
    # t = KG2Cypher(llm=llm, file_url=file_oss_url)
    # cypher = t.process(kg)
    # result["cypher"] = cypher
    callback({"type": "kg", "data": "inner cypher script", "step": "cypher"})

    # 将知识图谱导入到图数据库Neo4j中
    # execute_results = []
    # for k, v in cypher.items():
    #     res = neo4j.load_cypher(v)
    #     execute_results.append(res)

    callback({"type": "kg", "data": execute_results, "step": "execute"})

    result["execute_result"] = execute_results
    return result
