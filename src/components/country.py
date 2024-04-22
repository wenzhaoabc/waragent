import json
import re
from json import JSONDecodeError

from src.history.agent_actions import ActionType, Action
from src.history.profile import CountryProfile
from src.history.prompts import (
    p_situation,
    p_first_action_instruction,
    p_first_action_instruction_with_format,
)
from src.llm import LLM
from src.utils import log
from .board import Board
from .stick import Stick
from .secretary import SecretaryAgent


class CountryAgent(object):
    def __init__(
        self,
        identity: str,
        profile: CountryProfile,
        action_types: list[ActionType],
        secretary: SecretaryAgent,
        llm: LLM,
        board: Board,
        stick: Stick,
    ) -> None:
        self.identity = identity
        self.profile = profile
        self.action_types = action_types
        self.secretary = secretary
        self.llm = llm
        self.board = board
        self.stick = stick
        self.action_list = action_types
        self.actions_dict = {action.name: action for action in action_types}

    def filter_actions(self, actions: dict) -> tuple[list, bool]:
        """根据动作列表过滤出符合基本格式要求的动作"""
        # action name list
        action_name_list = [str(n).strip() for n in actions.keys()]
        # 剔除不在动作列表中的动作
        action_name_list = [
            n for n in action_name_list if n in self.actions_dict.keys()
        ]
        actions = {k: v for k, v in actions.items() if k in action_name_list}
        # 剔除包含空列表或为空的动作，即没有作用对象的动作
        # 对于input_type为empty的动作，v为{}, 需注意不可剔除
        actions = {k: v for k, v in actions.items() if v != []}

        # 对需要content的动作特殊处理
        success_flag = True
        contain_content_action_names = [
            a.name for a in self.action_list if a.require_content
        ]
        for name in action_name_list:
            if name in contain_content_action_names:
                if isinstance(actions.get(name), dict) and all(
                    "content" in list(country.values())[0]
                    for country in actions.get(name)
                ):
                    success_flag = True
                else:
                    success_flag = False
                    break
        # Wait Without Action 仅可单独出现，有其他动作时将其剔除
        if len(action_name_list) > 1 and "Wait Without Action" in action_name_list:
            action_name_list.remove("Wait Without Action")
        actions = {k: v for k, v in actions.items() if k in action_name_list}
        return actions, success_flag

    def generate_action(
        self, prompt: str, round_time: int = 0
    ) -> tuple[list[Action], list[Action], str, str]:
        """
        Generate action based on the prompt with LLM

        Args:
            prompt: The prompt for generating action
            round_time: The round time

        Returns:
            list[Action]: The new actions
            list[Action]: The response actions
            str: The thought process
            str: The original LLM response
        """
        try_count = 0
        while True:
            if try_count > 0:
                log.info(
                    f"Country {self.profile.country_name} occurs error in generating action. Try count: {try_count}"
                )

            if try_count > 3:
                log.error(
                    f"Country {self.profile.country_name} occurs error in generating action. Try count: {try_count}"
                )
                log.info(
                    f"generate plan error, return default action: {self.action_types[0].name}"
                )
                return (
                    "There is nothing special I need to do",
                    [
                        Action(
                            action_type=self.action_types[0],
                            action_input="",
                            properties={},
                        )
                    ],
                )

            llm_res = self.llm.chat(prompt, temperature=0.2)
            try_count += 1

            thought_process = llm_res.replace(r"(?s)```json.*?```", "")

            res_regex = r"```json(.*?)```"
            res = re.findall(res_regex, llm_res, re.DOTALL)
            success_flag = True
            if len(res) < 1:
                continue

            actions_str = [item.strip() for item in res[0]][0]
            try:
                actions = json.loads(actions_str)
                if not isinstance(actions, dict):
                    log.error("generate plan: error in json decode actions, not a list")
                    continue
            except TypeError | JSONDecodeError as e:
                log.warn(f"generate plan: error in json decode actions: {actions_str}")
                continue

            new_actions = {}
            response_actions = {}
            if round_time == 0:
                new_actions, success_flag = self.filter_actions(actions)
            else:
                if "response_actions" in actions.keys():
                    response_actions, success_flag = self.filter_actions(
                        actions.get("response_actions")
                    )
                if "new_actions" in actions.keys():
                    new_actions, success_flag = self.filter_actions(
                        actions.get("new_actions")
                    )

            if not success_flag:
                continue

            return (
                [
                    Action(
                        action_type=self.actions_dict.get(a),
                        action_input=actions.get(a),
                        properties={},
                    )
                    for a in new_actions.keys()
                ],
                [
                    Action(
                        action_type=self.actions_dict.get(a),
                        action_input=actions.get(a),
                        properties={},
                    )
                    for a in response_actions.keys()
                ],
                thought_process,
                actions_str,
            )

    def plan(self, initial_situation: str, current_situation: str) -> dict:
        plan_prompt = f"""
        {self.profile}
        {p_situation(initial_situation)}
        {p_first_action_instruction()}
        """

        secretary_check_times = 0
        secretary_agree = False

        while not secretary_agree:
            thought_process, actions, _, actions_str = self.generate_action(plan_prompt)
            error_action_name_suggestions = self.secretary.check_action_name(actions)
            error_action_input_suggestions = self.secretary.check_action_input(
                self.profile.country_name, actions
            )

            if error_action_name_suggestions or error_action_input_suggestions:
                # action name or action input error, regenerate action with new prompt
                plan_prompt = f"""{self.profile}
                {p_situation(initial_situation)}
                {p_first_action_instruction_with_format(actions_str, error_action_name_suggestions + error_action_input_suggestions)}"""
                continue

            pass
