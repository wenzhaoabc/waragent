import json
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.llm import LLM
from src.memory.board import Board
from src.memory.stick import Stick
from src.profiles import CountryProfile
from src.profiles.agent_actions import Action, ActionType
from src.prompts import country_prompt_v2 as cp_v2
from src.prompts.action_check import p_format_check, p_logic_check
from src.prompts.struct_format import Formatter, NlAction
from src.utils import log, extract_json, output
from .ministers import (
    FinanceMinister,
    ForeignMinister,
    MilitaryMinister,
    GeographyMinister,
)
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
        tool_choices: str = "auto",
        knowledge: str = "rag",
    ) -> None:
        self.profile = profile
        self.name = profile.country_name
        """国家名"""
        self.board = board
        self.stick = Stick(profile, profiles, board)
        self.secretary = SecretaryAgent(
            profile, profiles, action_types, board, self.stick
        )
        """秘书代理"""
        self.llm = llm
        self.ministers = {
            "Military Minister": MilitaryMinister(
                profile, profiles, action_types, llm, tool_choices, knowledge
            ),
            "Foreign Minister": ForeignMinister(
                profile, profiles, action_types, llm, tool_choices, knowledge
            ),
            "Finance Minister": FinanceMinister(
                profile, profiles, action_types, llm, tool_choices, knowledge
            ),
            "Geography Minister": GeographyMinister(
                profile, profiles, action_types, llm, tool_choices, knowledge
            ),
        }
        """国家大臣"""

        self.action_types = action_types
        """动作类型列表 [ ActionType ]"""

        self.actions_dict = {action.name: action for action in action_types}
        """动作名称字典 { action_name : ActionType }"""

    def fix_json(self, e: str, original_json: str) -> str:
        """借助LLM修复JSON格式上的错误"""
        prompt = (
            f"""This JSON string is something wrong when I try `json.loads()` in Python. The exception message is {e}"""
            "Please fix it. Thank you!\n"
            f"```json\n{original_json}\n```"
        )
        llm_res = self.llm.chat(prompt=prompt)
        actions_str = extract_json(llm_res)
        return actions_str

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
                if isinstance(actions.get(name), dict):
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

            match = re.search(
                r"Thought Process:\n(.*?)Actions in JSON format:", llm_res, re.DOTALL
            )
            if match:
                thought_process = match.group(1).strip()
            else:
                thought_process = "There is nothing special I need to do"

            res_regex = r"```json(.*?)```"
            res = re.findall(res_regex, llm_res, re.DOTALL)
            success_flag = True
            if len(res) < 1:
                continue

            actions_str = [item.strip() for item in res][0]
            try:
                actions = json.loads(actions_str)
                if not isinstance(actions, dict):
                    log.error("generate plan: error in json decode actions, not a list")
                    continue
            except Exception as e:
                log.warn(f"generate plan: error in json decode actions: {actions_str}")
                actions_str = self.fix_json(e.__str__(), actions_str)
                try:
                    actions = json.loads(actions_str)
                except Exception as e:
                    log.warn(
                        f"generate plan secondly: error in json decode actions: {actions_str}; exception:{e}"
                    )
                    continue

            log.info(f"No.{round_time} {self.name} generate actions : {actions}")
            new_actions = {}
            response_actions = {}
            if round_time == 1:
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
                        action_input=new_actions.get(a),
                        properties={},
                    )
                    for a in new_actions.keys()
                ],
                [
                    Action(
                        action_type=self.actions_dict.get(a),
                        action_input=response_actions.get(a),
                        properties={},
                    )
                    for a in response_actions.keys()
                ],
                thought_process,
                actions_str,
            )

    def generate_correct_format_actions(
        self, prompt: str, round_time: int
    ) -> tuple[list[Action], list[Action], str]:
        """借助秘书代理检查，生成符合格式要求的动作序列"""
        if round_time == 1:
            """第一回合，只检查new_actions"""
            action_check_times = 0
            new_prompt = prompt
            while True:
                new_actions, _, thought_process, raw_str = self.generate_action(
                    new_prompt, round_time
                )
                action_name_suggestions, correct_actions = (
                    self.secretary.check_action_name(new_actions)
                )
                action_input_suggestions, correct_actions = (
                    self.secretary.check_action_input(self.name, correct_actions)
                )
                action_check_times += 1
                suggestions = action_name_suggestions + action_input_suggestions

                if suggestions:

                    log.info(
                        f"No.{round_time} Round, {self.name} generates actions {new_actions} Suggestions: {suggestions}"
                    )
                    if action_check_times > 2:
                        new_actions = correct_actions
                        break
                    new_prompt = prompt + p_format_check(raw_str, suggestions)
                else:
                    break
            return new_actions, _, thought_process
        else:
            new_prompt = prompt
            action_check_times = 0
            while True:
                new_actions, response_actions, thought_process, raw_str = (
                    self.generate_action(new_prompt, round_time)
                )

                nans, nca = self.secretary.check_action_name(new_actions)
                nais, nca = self.secretary.check_action_input(self.name, nca)

                # response_action_name_suggestions, response_correct_actions
                rans, rca = self.secretary.check_action_name(response_actions)
                rais, rca = self.secretary.check_action_input(self.name, rca)

                action_check_times += 1
                suggestions = nans + nais + rans + rais
                if suggestions:
                    log.info(
                        f"No.{round_time} Round, {self.name} generates actions {new_actions},{response_actions} Suggestions: {suggestions}"
                    )
                    if action_check_times > 2:
                        new_actions = nca
                        response_actions = rca
                        break
                    new_prompt = prompt + p_format_check(raw_str, suggestions)
                else:
                    break
            return new_actions, response_actions, thought_process

    def first_plan(
        self, trigger: str, minister_advice: dict[str, str]
    ) -> tuple[list[NlAction], str]:
        """
        智能体进行第一次任务规划
        :param trigger: 战争模拟的触发事件
        :param minister_advice: 各位大臣的建议

        return : 动作序列
        """
        formatted_messages = []
        thought_process = ""
        # plan_prompt = p_first_action_instruction(
        #     self.profile, self.secretary.country_profiles, trigger
        # )
        plan_prompt = cp_v2.p_first_generate_actions(
            self.profile,
            self.secretary.country_profiles,
            self.action_types,
            current_situation=trigger,
            minister_advice=minister_advice,
            round_times=1,
        )
        try_count = 0
        secretary_agree = False
        while not secretary_agree:
            actions, _, thought_process = self.generate_correct_format_actions(
                plan_prompt, 1
            )
            log.info(f"No.1 round, {self.name} made actions: {actions}")

            formatted_messages = formatter.actions_format(self.name, actions)
            suggestions = self.secretary.check_active_action_logic(
                formatted_messages, self.stick, self.board
            )
            try_count += 1
            if suggestions:
                log.info(
                    f"No.1 round, {self.name} get logic suggestions: {suggestions}, tried {try_count}"
                )
                if try_count > 3:
                    formatted_messages = self.secretary.modify_new(
                        formatted_messages, self.stick, self.board
                    )
                    actions_str = formatter.nlaction_str(formatted_messages)
                    log.info(
                        f"No.1 round, secretary modified {self.name} actions: {actions_str}"
                    )
                    break
                actions_str = formatter.actions_to_json(actions)
                plan_prompt = plan_prompt + p_logic_check(actions_str, suggestions)
            else:
                secretary_agree = True
        return formatted_messages, thought_process

    def later_plan(
        self,
        round_time: int,
        trigger: str,
        current_situation: str,
        country_rels: str,
        received_requests: list[NlAction],
        minister_advice: dict[str, str],
    ) -> tuple[list[NlAction], list[NlAction], str]:
        new_formatted_messages = []
        res_formatted_messages = []
        thought_process = ""
        # plan_prompt = p_later_action_instruction(
        #     self.profile,
        #     self.secretary.country_profiles,
        #     round_time,
        #     action_history=action_histories,
        #     current_situation=current_situation,
        #     received_requests=received_requests_str,
        # )
        received_requests_str = "\n".join([rr.message for rr in received_requests])
        plan_prompt = cp_v2.p_later_generate_actions(
            self.profile,
            self.secretary.country_profiles,
            self.action_types,
            country_rels=country_rels,
            current_situation=current_situation,
            received_requests=received_requests_str,
            minister_advice=minister_advice,
            round_times=round_time,
        )
        try_count = 0
        secretary_agree = False
        while not secretary_agree:
            new_actions, res_actions, thought_process = (
                self.generate_correct_format_actions(plan_prompt, round_time)
            )
            log.info(
                f"No.{round_time} round, {self.name} made actions: {new_actions}, {res_actions}"
            )
            # 格式化为包含自然语言的描述
            res_formatted_messages = formatter.actions_format(self.name, res_actions)
            new_formatted_messages = formatter.actions_format(self.name, new_actions)

            # 首先查验回复类动作的逻辑性是否合理
            res_suggestions = self.secretary.check_response_action_logic(
                res_formatted_messages, received_requests
            )
            try_count += 1
            if res_suggestions:
                log.info(
                    f"No.{round_time} round, {self.name} res actions suggestions: {res_suggestions}"
                )
                actions_str = formatter.actions_to_json(new_actions, res_actions)
                if try_count > 3:
                    # 重复查验次数过多，直接对生成的不合理动作进行过滤
                    res_formatted_messages = self.secretary.modify_responses(
                        received_requests, res_formatted_messages
                    )
                    # 创建临时Board，根据智能体回复更新国家间关系，对new_actions进行过滤
                    temp_board = self.board.clone()
                    temp_board.update(res_formatted_messages, round_time)
                    new_formatted_messages = self.secretary.modify_new(
                        new_formatted_messages, self.stick, temp_board
                    )
                    break
                plan_prompt = plan_prompt + p_logic_check(actions_str, res_suggestions)
                continue

            # 回复动作逻辑上无误，查验新的主动动作的逻辑性
            temp_board = self.board.clone()
            temp_board.update(res_formatted_messages, round_time)
            new_suggestions = self.secretary.check_active_action_logic(
                new_formatted_messages, self.stick, temp_board
            )
            try_count += 1
            if new_suggestions:
                log.info(
                    f"No.{round_time} round, {self.name} new actions suggestions: {new_suggestions}"
                )
                if try_count > 3:
                    new_formatted_messages = self.secretary.modify_new(
                        received_requests, self.stick, temp_board
                    )
                    new_actions_str = formatter.nlaction_str(new_formatted_messages)
                    log.info(
                        f"No.1 round, secretary modified {self.name} new actions: {new_actions_str}"
                    )
                actions_str = formatter.actions_to_json(new_actions, res_actions)
                plan_prompt = plan_prompt + p_logic_check(actions_str, new_suggestions)
            else:
                secretary_agree = True
        return new_formatted_messages, res_formatted_messages, thought_process

    def generate_minister_questions(
        self,
        current_situation: str,
        received_requests: str,
    ) -> dict[str, str]:
        """根据当前状况向各位大臣提出请求意见"""
        prompt = cp_v2.p_ask_minister_instruction(
            self.profile,
            self.secretary.country_profiles,
            action_types=self.action_types,
            received_requests=received_requests,
            current_situation=current_situation,
        )
        llm_res = self.llm.chat(prompt, temperature=0.5)
        questions_str = extract_json(llm_res)
        try:
            questions = json.loads(questions_str)
        except Exception as e:
            log.info(f"generate minister questions failed: {questions_str}. try again.")
            questions_str = self.fix_json(e.__str__(), questions_str)
            try:
                questions = json.loads(questions_str)
            except Exception as e:
                questions = {
                    "Military Minister": "How many military weapons do we have, and what is the gap between our military strength and that of the enemy?",
                    "Finance Minister": "What is the economic condition of our country and can we sustain the war against our enemy?",
                    "Foreign Minister": "Which countries are our potential Allies, which countries are our potential enemies, and what is the military and economic strength of the potential enemies?",
                }
        return questions

    def async_interact(self, minister, q, current_situation, received_requests):
        return asyncio.to_thread(
            minister.interact, q, current_situation, received_requests
        )

    def get_minister_suggestions(
        self,
        questions: dict[str, str],
        current_situation: str,
        received_requests: str,
    ) -> dict[str, str]:

        async def gather_suggestions():
            res = {}
            tasks = []

            for m, q in questions.items():
                if m in self.ministers.keys():
                    task = self.async_interact(
                        self.ministers[m], q, current_situation, received_requests
                    )
                    tasks.append((m, task))
                else:
                    res[m] = f"{m} has no suggestions"

            results = await asyncio.gather(*[task for _, task in tasks])

            for (m, _), result in zip(tasks, results):
                res[m] = result

            return res

        # Run the async function and return its result
        return asyncio.run(gather_suggestions())

    def plan_v2(
        self, round_time: int, trigger: str, current_situation: str, dump_json: callable
    ):
        new_formatted_messages = []
        res_formatted_messages = []
        trigger = trigger.replace(self.name, "You")
        current_situation = current_situation.replace(self.name, "You")

        received_requests = self.board.get_country_requests(self.profile.country_name)
        received_requests_str = "\n".join([rr.message for rr in received_requests])

        if round_time > 1:
            dump_json(
                "process",
                round_time,
                {
                    "country": self.profile.country_name,
                    "received_requests": received_requests_str,
                },
            )

        ques_to_ministers = self.generate_minister_questions(
            current_situation,
            received_requests_str if round_time > 1 else "",
        )

        dump_json(
            "process",
            round_time,
            {"country": self.profile.country_name, "questions": ques_to_ministers},
        )

        output(
            "### President Questions:\n"
            + "\n".join(f"{m}\n{q}" for m, q in ques_to_ministers.items())
            + "\n\n"
        )
        minister_suggestions = self.get_minister_suggestions(
            ques_to_ministers,
            current_situation,
            received_requests_str if round_time > 1 else "",
        )
        output(
            "### Minister Suggestions:\n"
            + "\n".join(f"{m}\n{q}" for m, q in minister_suggestions.items())
            + "\n\n"
        )
        dump_json(
            "process",
            round_time,
            {"country": self.profile.country_name, "suggestions": minister_suggestions},
        )

        if round_time == 1:
            new_formatted_messages, thought_process = self.first_plan(
                trigger, minister_suggestions
            )
        else:
            current_situation = (
                self.stick.summary_internal_state() + "\n" + current_situation
            )
            country_rels = self.board.output_rels()
            new_formatted_messages, res_formatted_messages, thought_process = (
                self.later_plan(
                    round_time,
                    trigger,
                    current_situation,
                    country_rels=country_rels,
                    received_requests=received_requests,
                    minister_advice=minister_suggestions,
                )
            )

        self.stick.update(new_formatted_messages + res_formatted_messages)
        actions_data = formatter.actions_to_nl(
            new_formatted_messages, res_formatted_messages
        )
        dump_json(
            "process", round_time, {"actions": actions_data, "thought": thought_process}
        )
        output("### Thought Process:\n" + thought_process + "\n")

        return new_formatted_messages, res_formatted_messages
        # interact with secretary
