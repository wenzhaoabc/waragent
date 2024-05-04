"""
历史事件匿名化组件
将真实的国家名/历史事件进行替换
"""
from src.llm import LLM
from src.profiles import CountryProfile


class Anonymize:
    def __init__(self, llm: LLM, countries_profile: list[CountryProfile]):
        self.llm = llm
        self.countries_profile = countries_profile

    def get_system_prompt(self) -> str:
        prompt = (
            "You are an expert in history and linguistics."
            "You specialize in anonymizing historical events in simulations of historical events."
            "You will receive a historical text, and your task is to anonymize the historical event of this text."
            'You need to follow A certain rule to do this. Replace the actual country name with "Country" followed by a space followed by the first letter of the country. For example, replace "America" with "Country A".'
            'For City name replace with "City" plus space plus first letter of country plus first letter of city. For example, replace "Washington" with "City AW".'
            "Please output the anonymized result directly, do not output additional content."
        )
        return prompt

    def de_anonymize_prompt(self) -> str:
        prompt = (
            "You are an expert in history and linguistics."
            "Your task is to convert the anonymized historical information into real historical information."
            "The sentences you receive may include the names of countries such as Country U, Country J. Replace them with the real country name. "
            "Where A and J represent the first letter of a real Country's name, for example Country U stands for the United States and Country J stands for Japan. "
            "The actual country names involved can only be selected from the country names below.\n"
            f"{', '.join([c.real_name for c in self.countries_profile])}\n"
            "You need to make sure that the semantics of the statement are unchanged before and after the substitution."
            "Please output the anonymized result directly, do not output additional content."
        )
        return prompt

    def anonymize(self, input_txt: str) -> str:
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": input_txt}
        ]
        output = self.llm.generate(messages)
        return output

    def de_anonymize(self, input_txt: str) -> str:
        messages = [
            {"role": "system", "content": self.de_anonymize_prompt()},
            {"role": "user", "content": input_txt}
        ]
        output = self.llm.generate(messages)
        return output
