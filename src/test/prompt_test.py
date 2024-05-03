from src.prompts.country_prompt import *
from src.prompts.action_check import *
from src.profiles.profile_WWII import CountryProfileList
from src.prompts.minister_prompt import (
    p_minister_prompt,
)
from src.prompts.country_prompt_v2 import p_ask_minister_instruction


def TestCountryPrompt():
    """Country Profile Test"""
    p = p_countries_description(CountryProfileList[0], CountryProfileList)
    print(len(p))
    print(p)


def TestFormatCheckPrompt():
    error_str = """{"A":["A","S","D"],"Q":{"WE":"QAZ"}}"""
    suggestions = [
        "Error country name",
        "Error country name",
        "Error country name",
        "Error country name",
    ]
    p = p_format_check(error_str, suggestions)
    print(len(p))
    print(p)


def p_logic_check_test():
    error_str = """{"A":["A","S","D"],"Q":{"WE":"QAZ"}}"""
    suggestions = [
        "Error country name",
        "Error country name",
        "Error country name",
        "Error country name",
    ]
    p = p_logic_check(error_str, suggestions)
    print(len(p))
    print(p)


def p_first_action_instruction_test():
    trigger = "Country A killed the queen of Country B"
    p = p_first_action_instruction(CountryProfileList[0], CountryProfileList, trigger)
    print(len(p))
    print(p)


def p_later_action_instruction_test():
    current = "Country A killed the queen of Country B"
    p = p_later_action_instruction(
        CountryProfileList[0],
        CountryProfileList,
        round_time=3,
        action_history="Action history",
        current_situation="Current situation",
        received_requests="Received requests",
    )
    print(len(p))
    print(p)


def p_minister_prompt_test():
    p = p_minister_prompt(
        CountryProfileList[0], CountryProfileList, "Military Minister"
    )
    print(len(p))
    print(p)


def p_system_prompt_v2_test():
    from src.prompts.country_prompt_v2 import p_global_system_prompt

    p = p_global_system_prompt(
        CountryProfileList[0],
        CountryProfileList,
        [
            "Declare war",
            "Peace talk",
            "Adjust military budget",
            "Adjust diplomatic policy",
            "Adjust financial policy",
        ],
    )
    print(len(p))
    print(p)


def p_first_ask_minister_instruct_test():
    p = p_ask_minister_instruction(
        CountryProfileList[0],
        CountryProfileList,
        "Current situation",
        ActionTypeList,
    )
    print(len(p))
    print(p)


if __name__ == "__main__":
    p_first_ask_minister_instruct_test()
