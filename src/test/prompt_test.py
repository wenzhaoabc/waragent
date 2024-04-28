from src.prompts.country_prompt import *
from src.prompts.action_check import *
from src.profiles.profile_WWII import CountryProfileList


def TestCountryPrompt():
    """Country Profile Test"""
    p = p_countries_description(CountryProfileList[0], CountryProfileList)
    print(len(p))
    print(p)


def TestFormatCheckPrompt():
    error_str = """{"A":["A","S","D"],"Q":{"WE":"QAZ"}}"""
    suggestions = ["Error country name", "Error country name", "Error country name", "Error country name"]
    p = p_format_check(error_str, suggestions)
    print(len(p))
    print(p)


def p_logic_check_test():
    error_str = """{"A":["A","S","D"],"Q":{"WE":"QAZ"}}"""
    suggestions = ["Error country name", "Error country name", "Error country name", "Error country name"]
    p = p_logic_check(error_str, suggestions)
    print(len(p))
    print(p)


def p_first_action_instruction_test():
    trigger = "Country A killed the queen of Country B"
    p = p_first_action_instruction(CountryProfileList[0], CountryProfileList, trigger)
    print(len(p))
    print(p)


if __name__ == '__main__':
    p_first_action_instruction_test()
