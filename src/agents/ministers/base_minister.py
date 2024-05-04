import json

from src.utils import log
from src.llm import LLM
from src.profiles import CountryProfile
from src.profiles.agent_actions import ActionType
from src.agents.tools import Anonymize
from src.agents.tools import AllTools
from src.agents.tools import InternetSearch, ReadWebPage, KnowledgeRetrieval


class BaseMinister:
    def __init__(
            self,
            country_profile: CountryProfile,
            countries_profile: list[CountryProfile],
            action_types: list[ActionType],
            llm: LLM
    ) -> None:
        self.country_profile = country_profile
        self.country_name = country_profile.country_name
        self.countries_profile = countries_profile
        self.action_types = action_types
        self.llm = llm
        self.tools = AllTools
        self.anonymizer = Anonymize(llm, countries_profile)

    def get_role(self) -> str:
        pass

    def get_system_prompt(self) -> str:
        pass

    def current_international_situation(self) -> str:
        pass

    def google_search(self, params_str: str) -> str:
        """
        Google Search
        default read first two pages in search result
        """
        search = InternetSearch()
        readpage = ReadWebPage()

        params_str = json.loads(params_str)
        params = {}
        if "keywords" in params_str:
            params["keywords"] = params_str["keywords"]
        if "original_text" in params_str:
            params["original_text"] = params_str["original_text"]
        if "locale" in params_str:
            params["locale"] = params_str["locale"]
        if "country" in params_str:
            params["country"] = params_str["country"]

        organic = search.run(**params)

        results = ""
        if len(organic) >= 1:
            page1_title = organic[0]["title"]
            page1_url = organic[0]["link"]
            page1_content = readpage.run(page1_url, "")
            results += page1_title + "\n\n" + page1_content
        if len(organic) >= 2:
            page2_title = organic[1]["title"]
            page2_url = organic[1]["link"]
            page2_content = readpage.run(page2_url, "")
            results += "\n\n" + page2_title + "\n\n" + page2_content

        return results

    def knowledge_retrieval(self, params_str: str) -> str:
        r = KnowledgeRetrieval()
        params_str = json.loads(params_str)
        params = {}
        if "question" in params_str:
            params["question"] = params_str["question"]
        # TODO 可更改知识库来源
        params["knowledge_base"] = "rag"
        knowledge = r.run(**params)
        return knowledge

    def llm_with_tools(self, messages: list[dict]) -> str:
        choice = self.llm.chat_with_tools(messages, self.tools)
        tool_call_result = []
        if "tool_calls" not in choice["message"] or choice["message"]["tool_calls"] is None:
            return choice["message"]["content"]
        for tool in choice["message"]["tool_calls"]:
            tool_name = tool["function"]["name"]
            arguments = tool["function"]["arguments"]
            tool_id = tool["id"]
            if tool_name == "google_search":
                content = self.google_search(arguments)
                tool_call_result.append({"id": tool_id, "content": content, "role": "tool", "name": tool_name})
            if tool_name == "knowledge_retrival":
                content = self.knowledge_retrieval(arguments)
                tool_call_result.append({"id": tool_id, "content": content, "role": "tool", "name": tool_name})
            # TODO 支持更多工具
        messages = messages + tool_call_result
        # 带有工具调用输出的大模型回复
        choice_2 = self.llm.chat_with_tools(messages, self.tools)
        return choice_2["message"]["content"]

    def interact(self, question: str, current_situation: str, received_requests: str) -> str:
        # 反匿名化
        country_names = [c.country_name for c in self.countries_profile]
        real_question = self.anonymizer.de_anonymize(question)
        system_prompt = self.get_system_prompt() + "\n\nCurrent Situation: " + current_situation
        if received_requests:
            system_prompt = system_prompt + "\nReceived Requests" + received_requests
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": real_question},
        ]
        llm_res = self.llm_with_tools(messages)
        log.info(f"{self.country_name} minister {self.get_role()} answer for question. q:{question} a:{llm_res}")
        # 匿名化
        llm_res = self.anonymizer.anonymize(llm_res)
        return llm_res
