import json
import re
from json import JSONDecodeError

from src.history.agent_actions import ActionType, Action
from src.history.profile import CountryProfile
from src.history.prompts import (
    p_situation,
    p_first_action_instruction,
    p_first_action_instruction_with_logic,
    p_later_action_instruction,
    p_later_action_logic_check, p_action_format_check,
)
from src.llm import LLM
from src.utils import log
from .board import Board
from .secretary import SecretaryAgent
from .stick import Stick
from .struct_format import Formatter

formatter = Formatter(None)


class CountryAgent(object):
    def __init__(
            self,
            profile: CountryProfile,
            profiles: list[CountryProfile],
            action_types: list[ActionType],
            secretary: SecretaryAgent,
            llm: LLM,
            board: Board,
            stick: Stick,
    ) -> None:
        self.profile = profile
        self.name = profile.country_name
        """国家名"""
        self.secretary = SecretaryAgent(profile, profiles, action_types, board)
        """秘书代理"""
        self.llm = llm

        self.action_types = action_types
        """动作类型列表 [ ActionType ]"""
        self.board = board
        self.stick = stick

        self.actions_dict = {action.name: action for action in action_types}
        """动作名称字典 { action_name : ActionType }"""

    def filter_actions(self, actions: dict) -> tuple[dict, bool]:
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
            a.name for a in self.action_types if a.require_content
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
                    [
                        Action(
                            action_type=self.action_types[0],
                            action_input="",
                            properties={},
                        )
                    ],
                    [],
                    "There is nothing special I need to do",
                    "{}",
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

    def generate_correct_actions(
            self, prompt: str, round_time: int
    ) -> tuple[list[Action], list[Action]]:
        """借助秘书代理检查，生成符合格式要求的动作序列"""
        if round_time == 1:
            """第一回合，只检查new_actions"""
            action_check_times = 0
            new_prompt = prompt
            while True:
                new_actions, _, thought_process, raw_str = self.generate_action(new_prompt, round_time)
                action_name_suggestions, correct_actions = self.secretary.check_action_name(new_actions)
                action_input_suggestions, correct_actions = self.secretary.check_action_input(self.name,
                                                                                              correct_actions)
                action_check_times += 1
                suggestions = action_name_suggestions + action_input_suggestions

                if suggestions:
                    if action_check_times > 2:
                        new_actions = correct_actions
                        break
                    new_prompt = prompt + p_action_format_check(raw_str, suggestions)

                return new_actions, _

        else:
            new_prompt = prompt
            action_check_times = 0
            while True:
                new_actions, response_actions, thought_process, raw_str = self.generate_action(new_prompt, round_time)

                nans, nca = self.secretary.check_action_name(new_actions)
                nais, nca = self.secretary.check_action_input(self.name, nca)

                # response_action_name_suggestions, response_correct_actions
                rans, rca = self.secretary.check_action_name(response_actions)
                rais, rca = self.secretary.check_action_input(self.name, rca)

                action_check_times += 1
                suggestions = nans + nais + rans + rais
                if suggestions:
                    if action_check_times > 2:
                        new_actions = nca
                        response_actions = rca
                        continue
                    new_prompt = prompt + p_action_format_check(raw_str, suggestions)
                else:
                    return new_actions, response_actions

    def first_plan(self, trigger: str) -> list:
        """
        智能体进行第一次任务规划
        :param trigger: 战争模拟的触发事件

        return : 动作序列
        """
        pass

    def plan(
            self, initial_situation: str, current_situation: str, round_time: int
    ) -> list:
        if round_time == 1:
            plan_prompt = f"""
            {self.profile}
            {p_situation(initial_situation)}
            {p_first_action_instruction()}
            """

            secretary_check_times = 0
            secretary_agree = False
            while not secretary_agree:
                actions, _ = self.generate_correct_actions(plan_prompt, round_time)

                # formatted messages {"source": str, "action": str, "target": str, "message": str}
                formatted_messages = formatter.actions_format(self.name, actions)
                log.info(
                    f"Country {self.profile.country_name} plan: {formatted_messages}"
                )

                # 由秘书代理检查输入动作序列的逻辑性
                logic_suggestions = self.secretary.check_active_action_logic(
                    formatted_messages, self.stick, self.board
                )
                secretary_check_times += 1
                if logic_suggestions:
                    secretary_agree = False
                    if secretary_check_times > 3:
                        log.error(
                            f"Country {self.profile.country_name} plan: check action logic error, exceed max check times"
                        )
                        formatted_messages = self.secretary.modify_actions(
                            formatted_messages, self.stick, self.board
                        )
                        log.warn(
                            f"{self.profile.country_name} has planed error 3 times, and Secretary generate the default plan: {formatted_messages}"
                        )
                        break
                else:
                    log.info(
                        f"Secretary has agree the plan generated by {self.profile.country_name}, with action list: {formatted_messages}"
                    )
                    secretary_agree = True

                # TODO : communicate with secretary to modify the actions
                actions_str = formatter.actions_to_json(actions)
                plan_prompt = f"""{self.profile}
                {p_situation(initial_situation)}
                {p_first_action_instruction_with_logic(actions_str, logic_suggestions)}"""
        else:
            action_histories = self.board.get_past_history()
            received_requests = self.board.get_country_requests(
                self.profile.country_name
            )
            received_requests_str = "\n".join([rr.message for rr in received_requests])
            plan_prompt = f"""{self.profile}
{p_later_action_instruction(round_time, action_histories, current_situation, received_requests_str)}
{p_situation(current_situation)}"""

            secretary_response_check_times = 0
            secretary_action_check_times = 0
            secretary_agree = False

            while not secretary_agree:
                new_actions, response_actions = self.generate_correct_actions(plan_prompt, round_time)
                # 动作格式化为自然语言
                response_formatted_messages = formatter.actions_format(self.name, response_actions)
                new_formatted_messages = formatter.actions_format(self.name, new_actions)

                log.info(
                    f"Country {self.profile.country_name} plan: {response_formatted_messages} ; {new_formatted_messages}"
                )

                # 回复及新动作逻辑检查
                response_check_suggestions = self.secretary.check_response_action_logic(
                    received_requests, response_formatted_messages
                )
                secretary_response_check_times += 1
                formatted_messages = response_formatted_messages + new_formatted_messages
                if response_check_suggestions:
                    secretary_agree = False
                    suggestions = response_check_suggestions
                    if secretary_response_check_times > 1:
                        response_formatted_messages = self.secretary.modify_responses(
                            received_requests, response_formatted_messages
                        )
                if not response_check_suggestions or secretary_response_check_times > 1:
                    """智能体回复无误 or 超过一次智能体回复检查次数"""
                    # 根据智能体的回复更新历史状态 TODO 确定更新状态的时机， 此处更新是否会导致重复更新
                    # self.board.update(response_formatted_messages, round_time)
                    action_check_suggestions = self.secretary.check_active_action_logic(
                        new_formatted_messages, self.stick, self.board)
                    secretary_action_check_times += 1
                    if not action_check_suggestions:
                        formatted_messages = response_formatted_messages + new_formatted_messages
                        secretary_agree = True
                        log.info(
                            f"Secretary has checked the proposed actions by {self.profile.country_name} and agree with the actions list: {new_formatted_messages}"
                        )
                        break
                    else:
                        secretary_agree = False
                        suggestions = response_check_suggestions + action_check_suggestions
                        if secretary_action_check_times > 3:
                            log.info(
                                f"Secretary has checked 4 times and still not agree with the action list by {self.profile.country_name}, thus the Secretary directly modifies the action list."
                            )
                            new_formatted_messages = self.secretary.modify_actions(
                                new_formatted_messages, self.stick, self.board)
                            formatted_messages = response_formatted_messages + new_formatted_messages
                            secretary_agree = True
                            break
                log.info(
                    f"Secretary has checked and disagreed with the action list by {self.profile.country_name}. The secretary provides suggestions on how to generate."
                )
                plan_prompt = f"""{self.profile}\n\n{p_later_action_instruction(round_time, action_histories, current_situation, received_requests)}\n\n{p_situation(current_situation)}"""
                actions_str = formatter.actions_to_json(new_actions, response_actions)
                plan_prompt += p_later_action_logic_check(actions_str, suggestions)

        self.board.update(formatted_messages)
        return formatted_messages
