"""
Main function for the simulation
"""

import random
from concurrent.futures import ThreadPoolExecutor


from src.agents.country import CountryAgent
from src.llm import LLM
from src.memory.board import Board
from src.profiles.agent_actions import ActionTypeList
from src.profiles.profile_WWII import CountryProfileList
from src.memory.country_rel import CountryRel
from src.utils import log, output, initialize_pipe


def setup_board(board: Board, initial_status: list = []):
    """初始化国际关系"""
    for status in initial_status:
        country1 = status["country1"]
        country2 = status["country2"]
        if status["public"]:
            board.set_country_rel(
                country1,
                country2,
                CountryRel(status["rel"]),
                public=True,
            )
        else:
            board.set_country_rel(
                status["country1"],
                status["country2"],
                CountryRel(status["rel"]),
                public=False,
            )


def create_country_agent(args):
    """创建国家代理"""
    c, countries_profils, ActionTypeList, co_llm, board, tool_choice, knowledge = args
    return CountryAgent(
        c,
        countries_profils,
        ActionTypeList,
        co_llm,
        board,
        tool_choice,
        knowledge,
    )


def start_simulate(**kwargs):
    default = {
        "history": "II",
        "llm": "qwen-max-longcontext",
        "round": 10,
        "tool_choice": "auto",
        "knowledge": "rag",
        "trigger": "Country GE betray the Non-Intervention Treaty with Country PO and Country GE invasion of Country PO.",
        "countries": [c.country_name for c in CountryProfileList],
        "initial_status": [],
    }

    default.update(kwargs.get("config", {}))
    pipe = kwargs.get("pipe", None)
    llm_model = default["llm"]
    round_num = default["round"]
    trigger = default["trigger"]
    tool_choice = default["tool_choice"]
    knowledge = default["knowledge"]
    countries_profils = [
        c for c in CountryProfileList if c.country_name in default["countries"]
    ]
    print(default)

    board = Board(countries_profils)
    setup_board(board, default["initial_status"])

    co_llm = LLM(llm_model)
    args_countries = [
        (c, countries_profils, ActionTypeList, co_llm, board, tool_choice, knowledge)
        for c in countries_profils
    ]
    with ThreadPoolExecutor() as executor:
        countries = list(executor.map(create_country_agent, args_countries))
    # countries = [
    #     CountryAgent(
    #         c,
    #         countries_profils,
    #         ActionTypeList,
    #         co_llm,
    #         board,
    #         tool_choice,
    #         knowledge,
    #     )
    #     for c in countries_profils
    # ]

    dump_json = initialize_pipe(pipe)
    output(f"## Board:\n{board.output_rels()}")
    first = True
    for i in range(round_num):
        i += 1
        output(f"# Round {i}\n")
        dump_json("start", 1, {})
        countries_status = {
            c.country_name: {"mobilization": False} for c in countries_profils
        }
        dump_json(
            "status",
            i,
            {
                "rels": board.country_relations,
                "rels_pri": board.country_relations_private,
                "countries": countries_status,
            },
        )
        random.shuffle(countries)
        dump_json("country_order", i, {"order": [c.name for c in countries]})
        for country in countries:
            output(f"## {country.name}\n")
            countries_rels = board.summary_countries_rel(country.name, i)
            new_actions, res_actions = country.plan_v2(
                i,
                trigger=trigger,
                current_situation=countries_rels,
                dump_json=dump_json,
                first=first,
            )
            first = False
            output(f"### New Actions:\n{'\n'.join([a.message for a in new_actions])}\n")
            output(f"### Res Actions:\n{'\n'.join([a.message for a in res_actions])}\n")
            output(f"### Internal Statue:\n{country.stick.summary_internal_state()}\n")
            log.info(
                f"{country.profile.country_name} actions: {new_actions + res_actions}"
            )

            board.update(new_actions + res_actions, i + 1)
            countries_status = {
                c.name: {"mobilization": c.stick.mobilization} for c in countries
            }
            dump_json(
                "status",
                i,
                {
                    "rels": board.country_relations,
                    "rels_pri": board.country_relations_private,
                    "countries": countries_status,
                },
            )
            output(f"## Board:\n{board.output_rels()}\n")
            output(f"## Board Private:\n{board.output_rels_pri()}\n")
            output("\n")
        output(f"## Board:\n{board.output_rels()}\n")
        output(f"## Board Private:\n{board.output_rels_pri()}\n")
        output("\n\n")
        countries_status = {
            c.name: {"mobilization": c.stick.mobilization} for c in countries
        }
        dump_json(
            "status",
            i,
            {
                "rels": board.country_relations,
                "rels_pri": board.country_relations_private,
                "countries": countries_status,
            },
        )

    pipe.send("END")
    pipe.close()


# if __name__ == "__main__":
#     start_simulate(llm="gpt-4o")
