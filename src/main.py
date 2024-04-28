import random

from src.agents.country import CountryAgent
from src.llm import LLM
from src.memory.board import Board
from src.profiles.agent_actions import ActionTypeList
from src.profiles.profile_WWII import CountryProfileList


def main():
    board = Board(CountryProfileList)
    countries = [
        CountryAgent(c, CountryProfileList, ActionTypeList, LLM(), board)
        for c in CountryProfileList
    ]
    round_num = 10
    for i in range(round_num):
        random.shuffle(countries)
        for country in countries:
            actions = country.plan_v2(i + 1, "", current_situation="")
            board.update(actions, i + 1)


if __name__ == '__main__':
    main()
