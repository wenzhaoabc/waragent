"""
历史事件匿名化组件
将真实的国家名/历史事件进行替换
"""
from src.llm import LLM


class Anonymize:
    def __init__(self, llm: LLM):
        self.llm = llm

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

    def anonymize(self, input_txt: str) -> str:
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": input_txt}
        ]
        output = self.llm.generate(messages)
        return output

    def de_anonymize(self, country_real_names: list[str], input_txt: str) -> str:
        output = input_txt
        fake_real_names = {f"Country {n[0].upper()}": n for n in country_real_names}
        for fake, real in fake_real_names.items():
            output = output.replace(fake, real)
        return output

    def run(self, input_txt: str) -> str:
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": input_txt}
        ]
        output = self.llm.generate(messages)
        return output
