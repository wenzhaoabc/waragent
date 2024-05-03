from typing import Any, Dict, List

from src.llm import LLM


def remove_large_lists(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    The idea is to remove all properties that have large lists (embeddings) or text as values
    """
    LIST_CUTOFF = 56
    CHARACTER_CUTOFF = 5000
    # iterate over all key-value pairs in the dictionary
    for key, value in d.items():
        # if the value is a list and has more than list cutoff elements
        if isinstance(value, list) and len(value) > LIST_CUTOFF:
            d[key] = None
        # if the value is a string and has more than list cutoff elements
        if isinstance(value, str) and len(value) > CHARACTER_CUTOFF:
            d[key] = d[key][:CHARACTER_CUTOFF]
        # if the value is a dictionary
        elif isinstance(value, dict):
            # recurse into the nested dictionary
            remove_large_lists(d[key])
    return d


class SummarizeCypherResult:
    llm: LLM
    exclude_embeddings: bool

    def __init__(self, llm: LLM, exclude_embeddings: bool = True) -> None:
        self.llm = llm
        self.exclude_embeddings = exclude_embeddings

    def generate_user_prompt(self, question: str, results: List[Dict[str, str]]) -> str:
        return f"""
        The question was {question}
        Answer the question by using the following results:
        {results}
        """

    def generate_system_prompt(self) -> str:
        return (
            "You are an assistant that helps to generate text to form nice and human understandable answers based on the result of cypher queries."
            "You will get the question of human and the query results related to this question."
            "To ensure that your answers are correct, you should always refer to the results of your queries in your answers. Try to ensure that the structured results of your queries are translated into natural language that is easy for humans to understand."
        )

    def run(
            self,
            question: str,
            results: List[Dict[str, Any]],
    ) -> str:
        messages = [
            {"role": "system", "content": self.generate_system_prompt()},
            {"role": "user", "content": self.generate_user_prompt(question, results)},
        ]

        output = self.llm.generate(messages)
        return output
