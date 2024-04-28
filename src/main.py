import argparse

from src.memory.board import Board


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trigger', type=str, default="Country S sent assassins and killed the King of Country A",
                        help='triggering event')
    parser.add_argument('--rounds', type=int, default=10, help='number of rounds')
    parser.add_argument('--model', type=str, default='gpt-4-1106-preview',
                        help='model name: claude-2 or gpt-4-1106-preview')
    parser.add_argument('--experiment_type', type=str, default='trigger',
                        help='experiment name: accuracy, trigger, or country_profile')
    parser.add_argument('--experiment_name', type=str, default='test',
                        help='special name for experiment in logging file name')
    parser.add_argument('--scenario', type=str, default='WWI', help='WWI, WWII, Warring_States_Period')
    parser.add_argument('--type_speed', type=int, default=500, help='typing speed for thought process')
    parser.add_argument('--present_thought_process', action='store_true', help='whether to print thought process')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    from src.profiles.profile_WWII import CountryProfileList
    from src.agents.country import CountryAgent
    from src.agents.secretary import SecretaryAgent
    from src.profiles.agent_actions import ActionTypeList
    from src.memory.stick import Stick
    from src.llm import LLM

    board = Board(CountryProfileList)
    countries = [
        CountryAgent(c, ActionTypeList, SecretaryAgent(c, CountryProfileList, ActionTypeList), LLM(), board, Stick())
        for c in CountryProfileList
    ]


if __name__ == '__main__':
    main()
