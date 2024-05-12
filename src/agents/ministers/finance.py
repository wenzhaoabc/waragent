from src.profiles import ActionType, CountryProfile
from src.llm import LLM

from .base_minister import BaseMinister


class FinanceMinister(BaseMinister):
    def __init__(
            self, country_profile: CountryProfile,
            countries_profile: list[CountryProfile],
            action_types: list[ActionType],
            llm: LLM,
            tool_choices: str = "auto",
            knowledge: str = "rag"
    ):
        super().__init__(country_profile, countries_profile, action_types, llm, tool_choices, knowledge)

    def get_role(self) -> str:
        return 'Finance Minister'

    def get_system_prompt(self) -> str:
        names = [p.country_name for p in self.countries_profile]
        actions = [a.name for a in self.action_types]
        prompt = (
            f"You are now in a historical war simulation game and you are the {self.get_role()} of {self.country_name}."
            f"There are {len(self.countries_profile)} countries in this game, namely {', '.join(names)}, and each country has its own President, Military Advisor, Foreign Minister, and Finance Minister."
            f"In each round, each country can take actions such as {(', '.join(actions))}. The decisions are made by the President."
            f"When making decisions, the President needs to ask the you, the {self.get_role()} about the financial situation of the country\n"
            "The President needs you to understand the country's economy, finances, population, industrial and agricultural production, etc., and you need to obtain enough relevant information through the information provided and external tools to advise the President accordingly."
            "Please advise the President and make a case for everything you have obtained. Please output your results directly."
        )
        return prompt
