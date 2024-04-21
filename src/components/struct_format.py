# -*- coding: utf-8 -*-

from src.history.agent_actions import Action, ActionType, ActionInputType
from src.history.profile import CountryProfile


class Formatter:
    """
    This class is used to format the data in the neural language.
    将结构化的数据转为自然语言
    """

    def __init__(self, data):
        self.data = data

    def format(self):
        return self.data

    def actions_format(self, source_country: CountryProfile, actions: list[Action]) -> str:
        final_messages = []
        for a in actions:
            action_type = a.action_type
            action_name = action_type.name
            action_input = a.action_input
            action_input_type = action_type.input_type

            pass

        return self.data
