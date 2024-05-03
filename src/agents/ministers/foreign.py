from .base_minister import BaseMinister
from src.profiles import ActionType, CountryProfile
from src.llm import LLM


class ForeignMinister(BaseMinister):
    def __init__(
            self, country_profile: CountryProfile,
            countries_profile: list[CountryProfile],
            action_types: list[ActionType], llm: LLM
    ):
        super().__init__(country_profile, countries_profile, action_types, llm)

    def get_role(self) -> str:
        return 'Foreign Minister'

    def get_system_prompt(self) -> str:
        names = [p.country_name for p in self.countries_profile]
        actions = [a.name for a in self.action_types]
        prompt = (
            f"You are now in a historical war simulation game and you are the {self.get_role()} of {self.country_name}."
            f"There are {len(self.countries_profile)} countries in this game, namely {', '.join(names)}, and each country has its own President, Military Advisor, Foreign Minister, and Finance Minister."
            f"In each round, each country can take actions such as {(', '.join(actions))}. The decisions are made by the President."
            f"When making decisions, the President needs to ask the you, the {self.get_role()} about the country's Status of diplomacy.\n"
            "The president needs you to understand the country's potential Allies, potential enemies, and current threats."
            "The president also needs you to understand the military, economic and diplomatic situation of other countries."
            f"Your main task is to explain to the president what the country's foreign policy should be, that is, what it should do to other countries, and to explain your reasons in as much detail as possible."
            f"Please direct your advice to the president.\n"
        )
        return prompt
