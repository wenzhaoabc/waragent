import random

from src.agents.country import CountryAgent
from src.llm import LLM
from src.memory.board import Board
from src.profiles.agent_actions import ActionTypeList
from src.profiles.profile_WWII import CountryProfileList
from src.memory.country_rel import CountryRel
from src.utils import log, output


def get_trigger() -> str:
    return "Country J betray the Non-Intervention Treaty with Country P and Country J invasion of Country P."


def setup_board(board: Board):
    """初始化国际关系"""
    board.set_country_rel("Country J", "Country P", CountryRel.W)


def main():
    board = Board(CountryProfileList)
    setup_board(board)
    trigger = get_trigger()
    countries = [
        CountryAgent(c, CountryProfileList, ActionTypeList, LLM(), board)
        for c in CountryProfileList
    ]
    round_num = 10
    for i in range(round_num):
        i += 1
        output(f"# Round {i}\n\n")
        random.shuffle(countries)
        for country in countries:
            output(f"## {country.name}\n")
            countries_rels = board.summary_countries_rel(country.name, i)
            new_actions, res_actions = country.plan_v2(i, trigger=trigger, current_situation=countries_rels)
            output(f"### New Actions:\n{'\n'.join([a.message for a in new_actions])}\n")
            output(f"### Res Actions:\n{'\n'.join([a.message for a in res_actions])}\n")
            output(f"### Internal Statue:\n{country.stick.summary_internal_state()}\n")
            output("\n\n")
            log.info(f"{country.profile.country_name} actions: {new_actions + res_actions}")

            board.update(new_actions + res_actions, i + 1)
        output(f"## Board:\n{board.output_rels()}")
        output("\n\n")


if __name__ == "__main__":
    main()
