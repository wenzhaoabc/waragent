import json

from src.agents.tools import AllTools, Anonymize, InternetSearch, KnowledgeRetrieval, ReadWebPage
from src.llm import LLM
from src.profiles import CountryProfile
from src.profiles.agent_actions import ActionType
from src.utils import log
from src.prompts.country_prompt_v2 import p_countries_description

class BaseMinister:
    def __init__(
        self,
        country_profile: CountryProfile,
        countries_profile: list[CountryProfile],
        action_types: list[ActionType],
        llm: LLM,
        tool_choices: str = "auto",
        knowledge: str = "rag",
    ) -> None:
        self.country_profile = country_profile
        self.country_name = country_profile.country_name
        self.countries_profile = countries_profile
        self.action_types = action_types
        self.llm = llm
        self.tools = AllTools
        self.tool_choices = tool_choices
        self.knowledge = knowledge
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

        params_dict = json.loads(params_str)
        params = {}
        if "keywords" in params_dict:
            keywords = self.anonymizer.de_anonymize(params_dict["keywords"])
            params["keywords"] = keywords
        if "original_text" in params_dict:
            original_text = self.anonymizer.de_anonymize(params_dict["original_text"])
            params["original_text"] = original_text
        if "locale" in params_dict:
            params["locale"] = params_dict["locale"]
        if "country" in params_dict:
            params["country"] = params_dict["country"]

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

        log.info(
            f"Tool Google Search: params:{params_str}, anonymized_params: {json.dumps(params)}, urls:{json.dumps(organic)}"
        )
        anonymized_results = self.anonymizer.anonymize(results)
        return anonymized_results

    def knowledge_retrieval(self, params_str: str) -> str:
        r = KnowledgeRetrieval()
        params_dict = json.loads(params_str)
        params = {}
        if "question" in params_dict:
            question = self.anonymizer.de_anonymize(params_dict["question"])
            params["question"] = question
        # TODO 可更改知识库来源
        params["knowledge_base"] = self.knowledge
        knowledge = r.run(**params)
        anonymized_knowledge = self.anonymizer.anonymize(knowledge)
        log.info(
            f"Tool Knowledge Retrival: params:{params_str}, anonymized_params: {json.dumps(params)}"
        )
        return anonymized_knowledge

    def llm_with_tools(self, messages: list[dict]) -> str:
        choice = self.llm.chat_with_tools(messages, self.tools, self.tool_choices)
        choice = choice.model_dump()
        # choice = json.loads(choice)
        tool_call_result = []
        if (
            "tool_calls" not in choice["message"]
            or choice["message"]["tool_calls"] is None
        ):
            return choice["message"]["content"]
        tool_call_count = len(choice["message"]["tool_calls"])
        log.info(f'{self.get_role()} in {self.country_name} call tool count: {tool_call_count}')
        for tool in choice["message"]["tool_calls"]:
            tool_name = tool["function"]["name"]
            arguments = tool["function"]["arguments"]
            tool_id = tool["id"]
            content = ""
            if tool_name == "google_search":
                content = self.google_search(arguments)
                tool_call_result.append(
                    {
                        "tool_call_id": tool_id,
                        "content": content,
                        "role": "tool",
                        "name": tool_name,
                    }
                )
            if tool_name == "knowledge_retrival":
                content = self.knowledge_retrieval(arguments)
                tool_call_result.append(
                    {
                        "tool_call_id": tool_id,
                        "content": content,
                        "role": "tool",
                        "name": tool_name,
                    }
                )
            # TODO 支持更多工具
            log.info(
                f"{self.country_name} minister {self.get_role()} calls tools : {json.dumps({
                    "country": self.country_name, 
                    "role": self.get_role(), 
                    "tool":tool,
                    "function_result": content,
                    })}"
            )
        tool_call_messages = [choice["message"]]
        messages = messages + tool_call_messages + tool_call_result
        # 带有工具调用输出的大模型回复
        choice_2 = self.llm.chat_with_tools(messages, self.tools, self.tool_choices)
        choice_2 = choice_2.model_dump()
        return choice_2["message"]["content"]

    def interact(
        self, question: str, current_situation: str, received_requests: str
    ) -> str:
        user_prompt = (
            "Current Situation: \n" + current_situation
        )
        if received_requests:
            user_prompt = user_prompt + "Received Requests: \n" + received_requests
        user_prompt = user_prompt +"Questions From President:\n"+ question + "Please provide your analysis and advice."
        system_prompt = self.get_system_prompt() + "\n\nThe following is the profiles of the countries :\n" + p_countries_description(self.country_profile, self.countries_profile) + "\n\n"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        # 直接调用大模型
        llm_res = self.llm.generate(messages)
        log.info(
            f"{self.country_name} minister {self.get_role()} answer for question : {json.dumps({"question": question, "answer": llm_res})}"
        )
        return llm_res
