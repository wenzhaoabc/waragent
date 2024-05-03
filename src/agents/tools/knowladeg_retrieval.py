from typing import Literal
from src.datasource import Neo4jAnswers, RAG


class KnowledgeRetrieval:
    definition = {
        "type": "function",
        "function": {
            "name": "knowledge_retrival",
            "description": "Search the war game knowledge base to get all the military and economic information about your country and other countries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Questions that require relevant answers from the knowledge base.",
                    },
                },
                "required": ["question"],
            },
        },
    }

    def __init__(self):
        pass

    def run(self, question: str, knowledge_base: Literal["kg", "rag"] = "kg") -> str:
        if knowledge_base == "kg":
            neo4j = Neo4jAnswers()
            answer = neo4j.neo4j_answers(question)
            return answer
        elif knowledge_base == "rag":
            r = RAG()
            answer = r.retrival(question)
            return answer
        return ""
