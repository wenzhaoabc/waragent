import random

from src.agents.country import CountryAgent
from src.llm import LLM
from src.memory.board import Board
from src.profiles.agent_actions import ActionTypeList
from src.profiles.profile_WWII import CountryProfileList
from src.memory.country_rel import CountryRel
from src.utils import log, output, initialize_pipe


def get_trigger() -> str:
    return "Country J betray the Non-Intervention Treaty with Country P and Country J invasion of Country P."


def setup_board(board: Board):
    """初始化国际关系"""
    board.set_country_rel("Country J", "Country P", CountryRel.W)


def start_simulate(**kwargs):
    default = {
        "history": "II",
        "llm": "qwen-plus",
        "round": 10,
        "tool_choice": "auto",
        "knowledge": "rag",
        "trigger": "Country J betray the Non-Intervention Treaty with Country P and Country J invasion of Country P."
    }
    default = kwargs.get("config")
    pipe = kwargs.get("pipe")
    llm_model = default["llm"]
    round_num = default["round"]
    trigger = default["trigger"]
    tool_choice = default["tool_choice"]
    knowledge = default["knowledge"]

    board = Board(CountryProfileList)
    setup_board(board)

    countries = [
        CountryAgent(c, CountryProfileList, ActionTypeList, LLM(llm_model), board, tool_choice, knowledge)
        for c in CountryProfileList
    ]

    dump_json = initialize_pipe(pipe)

    for i in range(round_num):
        i += 1
        output(f"# Round {i}\n\n")
        dump_json("start", 1, {})
        countries_status = {c.country_name: {"mobilization": False} for c in CountryProfileList}
        dump_json("status", 1, {
            "rels": board.country_relations,
            "rels_pri": board.country_relations_private,
            "countries": countries_status
        })
        random.shuffle(countries)
        for country in countries:
            output(f"## {country.name}\n")
            countries_rels = board.summary_countries_rel(country.name, i)
            new_actions, res_actions = country.plan_v2(i,
                                                       trigger=trigger,
                                                       current_situation=countries_rels,
                                                       dump_json=dump_json)
            output(f"### New Actions:\n{'\n'.join([a.message for a in new_actions])}\n")
            output(f"### Res Actions:\n{'\n'.join([a.message for a in res_actions])}\n")
            output(f"### Internal Statue:\n{country.stick.summary_internal_state()}\n")
            output("\n\n")
            log.info(f"{country.profile.country_name} actions: {new_actions + res_actions}")

            board.update(new_actions + res_actions, i + 1)
        output(f"## Board:\n{board.output_rels()}")
        output("\n\n")
        countries_status = {{c.name: {"mobilization": c.stick.mobilization}} for c in countries}
        dump_json("status", i, {
            "rels": board.country_relations,
            "rels_pri": board.country_relations_private,
            "countries": countries_status
        })
