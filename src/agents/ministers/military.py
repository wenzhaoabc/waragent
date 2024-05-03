from src.profiles import ActionType, CountryProfile
from src.llm import LLM

from .base_minister import BaseMinister


class MilitaryMinister(BaseMinister):
    def __init__(
            self, country_profile: CountryProfile,
            countries_profile: list[CountryProfile],
            action_types: list[ActionType], llm: LLM
    ):
        super().__init__(country_profile, countries_profile, action_types, llm)

    def get_role(self) -> str:
        return "Military Minister"

    def get_system_prompt(self) -> str:
        actions = [a.name for a in self.action_types]
        # 在这场游戏中，共有 3 个国家，分别是美国、中国和俄罗斯，每个国家都有自己的军事大臣、外交大臣和财政大臣。
        # 在每一轮的交互中，每个国家可以做出的动作包括：宣战、和谈、调整军费、调整外交政策、调整财政政策等。决策由总统做出。
        # 总统在做出决策时，需要向军事大臣询问国家的军事情况及军事建议。
        # 你需要针对总统的问题总结国内的军事情况及与其它国家的军事对比，提出军事建议。
        # 总统做出决策后，你也可以提出自己的看法和建议。
        # 你可以调用外部工具辅助完成你的工作
        names = [p.country_name for p in self.countries_profile]
        prompt = (
            f"You are now in a historical war simulation game and you are the {self.get_role()} of {self.country_name}."
            f"There are {len(self.countries_profile)} countries in this game, namely {', '.join(names)}, and each country has its own President, Military Advisor, Foreign Minister, and Finance Minister."
            f"In each round, each country can take actions such as {(', '.join(actions))}. The decisions are made by the President."
            "When making decisions, the President needs to ask the Military Advisor about the country's military situation and military advice."
            "Your main task is to provide military advice to the President, and to provide advice on military strategy and tactics."
            "After the President makes a decision, you can also provide your own views and suggestions."
            "You can use external tools to help you complete your work."
            "Please direct your advice to the president.\n"
        )
        return prompt
