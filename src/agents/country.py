import json
import re
from json import JSONDecodeError

from src.llm import LLM
from src.memory.board import Board
from src.memory.stick import Stick
from src.profiles.agent_actions import Action, ActionType
from src.profiles.agent_profile import CountryProfile
from src.prompts.action_check import p_format_check, p_logic_check
from src.prompts.country_prompt import (
    p_first_action_instruction,
    p_later_action_instruction,
)
from src.prompts.struct_format import Formatter, NlAction
from src.utils import log
from .secretary import SecretaryAgent

formatter = Formatter(None)


class CountryAgent(object):
    def __init__(
            self,
            profile: CountryProfile,
            profiles: list[CountryProfile],
            action_types: list[ActionType],
            llm: LLM,
            board: Board,
    ) -> None:
        self.profile = profile
        self.name = profile.country_name
        """国家名"""
        self.board = board
        self.stick = Stick(profile, profiles, board)
        self.secretary = SecretaryAgent(profile, profiles, action_types, board, self.stick)
        """秘书代理"""
        self.llm = llm

        self.action_types = action_types
        """动作类型列表 [ ActionType ]"""

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

    def generate_correct_format_actions(
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
                    log.info(
                        f"No.{round_time} Round, {self.name} generates actions {new_actions} Suggestions: {suggestions}")
                    if action_check_times > 2:
                        new_actions = correct_actions
                        break
                    new_prompt = prompt + p_format_check(raw_str, suggestions)
                else:
                    break
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
                    log.info(
                        f"No.{round_time} Round, {self.name} generates actions {new_actions},{response_actions} Suggestions: {suggestions}")
                    if action_check_times > 2:
                        new_actions = nca
                        response_actions = rca
                        break
                    new_prompt = prompt + p_format_check(raw_str, suggestions)
                else:
                    break
            return new_actions, response_actions

    def first_plan(self, trigger: str) -> list[NlAction]:
        """
        智能体进行第一次任务规划
        :param trigger: 战争模拟的触发事件

        return : 动作序列
        """
        formatted_messages = []
        plan_prompt = p_first_action_instruction(self.profile, self.secretary.country_profiles, trigger)
        try_count = 0
        secretary_agree = False
        while not secretary_agree:
            actions, _ = self.generate_correct_format_actions(plan_prompt, 1)
            log.info(f"No.1 round, {self.name} made actions: {actions}")

            formatted_messages = formatter.actions_format(self.name, actions)
            suggestions = self.secretary.check_active_action_logic(formatted_messages, self.stick, self.board)
            try_count += 1
            if suggestions:
                log.info(f"No.1 round, {self.name} get logic suggestions: {suggestions}, tried {try_count}")
                if try_count > 3:
                    formatted_messages = self.secretary.modify_new(formatted_messages, self.stick, self.board)
                    actions_str = formatter.nlaction_str(formatted_messages)
                    log.info(f"No.1 round, secretary modified {self.name} actions: {actions_str}")
                    break
                actions_str = formatter.actions_to_json(actions)
                plan_prompt = plan_prompt + p_logic_check(actions_str, suggestions)
            else:
                secretary_agree = True
        return formatted_messages

    def later_plan(
            self, round_time: int, trigger: str, current_situation: str
    ) -> list[NlAction]:
        formatted_messages = []
        action_histories = self.board.get_past_history()
        received_requests = self.board.get_country_requests(self.profile.country_name)
        received_requests_str = "\n".join([rr.message for rr in received_requests])
        plan_prompt = p_later_action_instruction(
            self.profile, self.secretary.country_profiles, round_time,
            action_history=action_histories,
            current_situation=current_situation,
            received_requests=received_requests_str,
        )
        try_count = 0
        secretary_agree = False
        while not secretary_agree:
            new_actions, res_actions = self.generate_correct_format_actions(plan_prompt, round_time)
            log.info(f"No.{round_time} round, {self.name} made actions: {new_actions}, {res_actions}")
            # 格式化为包含自然语言的描述
            res_formatted_messages = formatter.actions_format(self.name, res_actions)
            new_formatted_messages = formatter.actions_format(self.name, new_actions)

            # 首先查验回复类动作的逻辑性是否合理
            res_suggestions = self.secretary.check_response_action_logic(res_formatted_messages, received_requests)
            try_count += 1
            if res_suggestions:
                log.info(f"No.{round_time} round, {self.name} res actions suggestions: {res_suggestions}")
                actions_str = formatter.actions_to_json(new_actions, res_actions)
                if try_count > 3:
                    # 重复查验次数过多，直接对生成的不合理动作进行过滤
                    res_formatted_messages = self.secretary.modify_responses(received_requests, res_formatted_messages)
                    # 创建临时Board，根据智能体回复更新国家间关系，对new_actions进行过滤
                    temp_board = self.board.clone()
                    temp_board.update(res_formatted_messages, round_time)
                    new_formatted_messages = self.secretary.modify_new(new_formatted_messages, self.stick, temp_board)
                    break
                plan_prompt = plan_prompt + p_logic_check(actions_str, res_suggestions)
                continue

            # 回复动作逻辑上无误，查验新的主动动作的逻辑性
            temp_board = self.board.clone()
            temp_board.update(res_formatted_messages, round_time)
            new_suggestions = self.secretary.check_active_action_logic(new_formatted_messages, self.stick, temp_board)
            try_count += 1
            if new_suggestions:
                log.info(f"No.{round_time} round, {self.name} new actions suggestions: {new_suggestions}")
                if try_count > 3:
                    new_formatted_messages = self.secretary.modify_new(received_requests, self.stick, temp_board)
                    new_actions_str = formatter.nlaction_str(new_formatted_messages)
                    log.info(f"No.1 round, secretary modified {self.name} new actions: {new_actions_str}")
                actions_str = formatter.actions_to_json(new_actions, res_actions)
                plan_prompt = plan_prompt + p_logic_check(actions_str, new_suggestions)
            else:
                secretary_agree = True
            formatted_messages = new_formatted_messages + res_formatted_messages
        return formatted_messages

    def plan_v2(self, round_time: int, trigger: str, current_situation: str):
        formatted_messages = []
        if round_time == 1:
            formatted_messages = self.first_plan(trigger)
        else:
            formatted_messages = self.later_plan(round_time, trigger, current_situation)

        self.stick.update(formatted_messages)

        # interact with secretary
