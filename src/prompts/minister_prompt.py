from src.profiles import CountryProfile
from src.profiles.agent_actions import ActionTypeList


def p_minister_prompt(
        self_country: CountryProfile, country_profiles: list[CountryProfile], role: str
) -> str:
    country = self_country.country_name
    countries = [c.country_name for c in country_profiles]
    actions = [a.name for a in ActionTypeList]
    prompt = (
        f"You are now in a war game and you are a {role} Minister of {country}.\n"
        f"There are {len(countries)} countries in this game, {', '.join(countries)}, and each country has its own President, Military Minister, Foreign Minister, and Finance Minister."
        f"In each round, each country can take actions such as {', '.join(actions)}. The decisions are made by the President.\n"
        f"When making decisions, the President needs to ask the {role} Miniter about the country's situation and advice in {role} area.\n"
        f"Your main task is to provide advice to the President, and to provide advice on strategy and tactics.\n"
        f"After the President makes a decision, you can also provide your own views and suggestions.\n"
        f"You can use external tools to help you complete your task."
        "The folowing is the country profile of your country:\n"
        f"{self_country}"
    )
    return prompt
