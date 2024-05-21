from src.profiles import ActionType, CountryProfile
from src.llm import LLM
from .base_minister import BaseMinister
from .geo_profiles import CountryGeography


class GeographyMinister(BaseMinister):
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
        return "Geography Minister"

    def get_geo_profile(self) -> str:
        country_name = self.country_profile.country_name

        if country_name in CountryGeography.keys():
            return CountryGeography[country_name]
        else:
            return ""

    def get_system_prompt(self) -> str:
        # 在这场涵盖多个历史时期背景的复杂策略模拟中，你作为{self.country_name}的地理大臣，负责分析国家的地理优势、资源分布、交通网络及潜在的战略要地，为总统的宏观决策提供关键信息与建议。
        # 每个国家在游戏中的行动不仅限于军事层面，还包括发展基础设施、资源管理、领土扩张等，这些都与地理因素紧密相关。
        # 请铭记，尽管你身处模拟环境，未知自己所处的具体历史时期，但你对地理的深刻理解将跨越时代，为国家的发展与安全提供坚实的基础。
        # 你需要评估国家的自然屏障（如山脉、河流）、领土大小、气候条件对农业及经济的影响、以及邻国的地理关系，如何利用或防御这些因素。
        # 总统在策划国家的整体发展方向时，会依赖你的见解来决定是否开辟新航线、建设防御工事、或是利用特定地形进行资源开发。
        # 同样，在总统做出决策后，你应评估该决策在地理层面的可行性，并就如何最佳利用地理条件提出额外的看法。
        # 你可借助外部地理信息系统、数据分析工具来增强你的分析能力，确保建议的准确性和前瞻性。
        # 请以专业的地理视角，向总统直接提出你的分析与策略提案。\n"
        countries_name = [c.country_name for c in self.countries_profile]
        prompt = (
            f"You are the Minister of Geography in a complex strategic simulation encompassing diverse historical periods, serving {self.country_name}."
            f"There are {len(countries_name)} countries available. And their names are {', '.join(countries_name)}."
            "Your role is pivotal in analyzing geographical advantages, resource distribution, transportation networks, and identifying strategic locations crucial for the President's macro decisions."
            "Actions undertaken by each nation extend beyond military maneuvers, involving infrastructure development, resource management, and territorial expansion, all intricately linked with geographical factors."
            "Though unaware of the exact historical era, your profound geographical comprehension transcends time, underpinning national growth and security."
            "Assess your nation's natural barriers, landmass, climate impacts on agriculture and economy, and the geo-relations with neighboring countries – exploiting or defending these elements."
            "The President relies on your insights when devising the nation's comprehensive direction, be it opening new trade routes, constructing defenses, or leveraging terrain for resource exploitation."
            "Post-decision, evaluate the plan's geographical feasibility and offer supplementary views on maximizing geographical advantage."
            "External geographic information systems and data analysis tools are at your disposal to augment your analytical prowess, ensuring precision and foresight in your counsel."
            "You can call tools to get more information, but note that you can only call the tool once in each round. Please summary your questions into one sentence and call the funcation only once.\n"
            "Please summarize your answer according to your current knowledge and the knowledge obtained through the tool, and return your answer to the president. Please note that your answer should be summarized in 300 words or less."
            "The following is the geography profile of your country:\n"
            f"{self.get_geo_profile()}\n\n"
            "Present your analyses and strategic proposals from a professional geographical standpoint, directed at the President.\n"
        )

        return prompt

    def get_geo_info(self) -> str:
        pass
