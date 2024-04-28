import random

from src.utils import log
from src.profiles.agent_profile import CountryProfile
from src.profiles.agent_actions import Action, ActionInputType, ActionType
from src.memory.board import Board
from src.memory.stick import Stick
from src.prompts.struct_format import NlAction
from src.memory.country_rel import CountryRel


class SecretaryAgent:
    """
    秘书代理
    """

    def __init__(
            self,
            country: CountryProfile,
            country_profiles: list[CountryProfile],
            action_types: list[ActionType],
            board: Board,
            stick: Stick,
    ) -> None:
        self.country = country
        self.name = country.country_name

        self.country_profiles = country_profiles
        """所有国家的profile"""
        self.country_names = [country.country_name for country in self.country_profiles]
        """所有国家的国家名"""

        self.action_types = action_types
        self.board = board
        self.stick = stick

    def check_action_name(self, actions: list[Action]) -> tuple[list[str], list[Action]]:
        """
        检查动作名称
        Args:
            actions: 原始动作输入
        Return:
            动作输入修正建议列表，剔除不合理动作后的动作列表
        """
        suggestions = []
        correct_actions = []
        for action in actions:
            if action.name not in [a.name for a in self.action_types]:
                suggestions.append(
                    f"Invalid action name {action.action_type.name} Action {action.action_type.name} is not in the action list."
                )
            else:
                correct_actions.append(action.name)
        log.info(f"Check action name suggestions: {suggestions}")
        return suggestions, correct_actions

    def check_action_input(
            self, source_country: str, actions: list[Action]
    ) -> tuple[list[str], list[Action]]:
        """
        检查动作输入是否满足要求

        Args:
            source_country: 动作来源国家
            actions: 动作列表
        Returns:
            建议列表，修正后的动作列表
        """
        suggestions = []
        correct_actions = []
        for action in actions:
            action_type = action.action_type
            action_name = action_type.name
            action_input = action.action_input

            if action_type.input_type == ActionInputType.empty:
                correct_actions.append(Action(action_type=action_type, action_input="", properties={}))
                if not action_input:
                    suggestions.append(f"Invalid action input : the input of {action_type.name} should be empty.")

            elif action_type.input_type == ActionInputType.country_list:
                """输入要求为国家名列表，剔除不存在的国家名"""
                if not isinstance(action_input, list):
                    suggestions.append(f"Invalid action input : the input of {action_type.name} should be a list.")
                    correct_actions.append(Action(action_type=action_type, action_input=[], properties={}))
                    continue

                error_country_names = [cn for cn in action_input if cn not in self.country_names or cn == self.name]
                if self.name in error_country_names:
                    suggestions.append(
                        f"You are {self.name}. The target countries of {action_name} should not contain itself."
                    )
                error_country_names.remove(self.name)
                suggestions.append(
                    f"Invalid action input for {action_name} : {', '.join(error_country_names)}. These countries do not exist."
                )
                correct_actions.append(
                    Action(
                        action_type=action_type,
                        action_input=list(set(action_input) - set(error_country_names) - set(self.country_names)),
                        properties={}
                    ))
            elif action_type.input_type == ActionInputType.country_tuple_list:
                """输入要求为国家名的二维列表，暂时不存在这种输入"""
                pass
            elif action_type.input_type == ActionInputType.country_dict:
                """输入要求为国家名为key的键值对，剔除不存在的键，content键不存在的设为空字符串"""
                if not isinstance(action_input, dict):
                    suggestions.append(f"Invalid action input : the input of {action_type.name} should be a dict.")
                    continue
                error_country_names = [cn for cn in action_input.keys() if
                                       cn not in self.country_names or cn == self.name]
                suggestions.append(
                    f"Invalid action input : {', '.join(error_country_names)}. These countries do not exist."
                )
                action_input = {k: v for k, v in action_input.items() if k not in error_country_names}
                for k, v in action_input.items():
                    if not isinstance(v, dict):
                        suggestions.append(
                            f"Invalid action input : the action input for {action_name} to {k} should be a dict containing a \"content\" key."
                        )
                        continue
                    if v.get("content") is None:
                        suggestions.append(
                            f"Invalid action input : the action input for {action_name} to {k} should contain a \"content\" key."
                        )
                        continue
                    correct_actions.append(
                        Action(action_type=action_type, action_input=v, properties={})
                    )

        return suggestions, correct_actions

    def check_active_action_logic(
            self, activated: list[NlAction], stick: Stick, board: Board
    ) -> list[str]:
        """
        检查动作逻辑是否满足要求

        Args:
            activated: 自然语言格式化的动作列表
            stick: 国家代理专属信息库
            board: 公共信息库

        Returns:
            list[str]: 建议列表
        """

        suggestions = []
        for nlaction in activated:
            source_country = nlaction.source
            if source_country != self.name:
                raise ValueError("Invalid source country.")
            action_name = nlaction.action
            target_country = nlaction.target

            if not target_country:
                if action_name == "General Mobilization" and stick.get_mob():
                    suggestions.append(
                        f"Invalid action: {source_country} has already mobilized."
                    )
                continue

            # 不可向同一个国家重复宣战
            # 已达成的协议需要先违约再宣战
            if action_name == "Declare War":
                if board.get_rel_pri(source_country, target_country) == CountryRel.W:
                    suggestions.append(
                        f"Invalid action: {source_country} has already declared war on {target_country}."
                    )
                if board.get_rel_pri(source_country, target_country) == CountryRel.M:
                    suggestions.append(
                        f"Invalid action: {source_country} has already formed b military alliance with {target_country}. You should betray it first."
                    )
                if board.get_rel_pri(source_country, target_country) == CountryRel.T:
                    suggestions.append(
                        f"Invalid action: {source_country} has already signed b non-intervention treaty with {target_country}. You should betray it first."
                    )
                if board.get_rel_pri(source_country, target_country) == CountryRel.P:
                    suggestions.append(
                        f"Invalid action: {source_country} has already signed b peace agreement with {target_country}. You should betray it first."
                    )
            if "Publish " in action_name:
                action_rel_dict = {
                    "Publish Military Alliance": CountryRel.M,
                    "Publish Non-intervention Treaty": CountryRel.T,
                    "Publish Peace Agreement": CountryRel.P,
                }
                for action, rel in action_rel_dict.items():
                    if action_name == action and board.get_rel_pri(source_country, target_country) != rel:
                        suggestions.append(
                            f"{source_country} currently cannot {action} as {source_country} and {target_country} have not formed {action.replace("Publish ", "")}. You need to make diplomatic effort."
                        )

            if "Betray " in action_name:
                action_rel_dict = {
                    "Betray Military Alliance": CountryRel.M,
                    "Betray Non-intervention Treaty": CountryRel.T,
                    "Betray Peace Agreement": CountryRel.P,
                }
                for action, rel in action_rel_dict.items():
                    if action_name == action and board.get_rel_pri(source_country, target_country) != rel:
                        suggestions.append(
                            f"{source_country} currently cannot {action} as {source_country} and {target_country} have not formed {action.replace("Betray ", "")}. "
                        )

            if "Request " in action_name:
                action_rel_dict = {
                    "Request Military Alliance": CountryRel.M,
                    "Request Non-intervention Treaty": CountryRel.T,
                    "Request Peace Agreement": CountryRel.P,
                }
                for action, rel in action_rel_dict.items():
                    if action_name == action and board.get_rel_pri(source_country, target_country) != rel:
                        suggestions.append(
                            f"{source_country} currently cannot {action} as {source_country} and {target_country} have already formed {action.replace("Request ", "")}. "
                        )

        # 针对结盟的国家，当有一方处于战争状态时，另一方需要发动战争或者违约
        # 获取所有结盟的国家
        alliance_countries = board.get_countries_with_rel_pub(self.name, CountryRel.M)
        for b in alliance_countries:
            for c in board.get_countries_with_rel_pub(b, CountryRel.W):
                if board.get_rel_pub(self.name, c) != CountryRel.W:
                    suggestions.append(
                        f"Your military alliance Country {b} is already in war with Country {c} but your Country {self.name} has not declared war. You should either Declare War against Country {c} or Betray Military Alliance with Country {b}."
                    )

        suggestions = list(set(suggestions))
        return suggestions

    def modify_new(
            self, activated: list[NlAction], stick: Stick, board: Board
    ) -> list[NlAction]:
        """
        修正智能体的主动动作

        Args:
            activated: 动作列表
            stick: 国家代理专属信息库
            board: 公共信息库

        Returns:
            list[NlAction]: 修正后的动作列表
        """
        filtered_actions = []
        for action in activated:
            this_source_country = action.source
            this_action_name = action.action
            this_target_country = action.target

            # 如果没有目标国家，且动作为动员，则只有当未动员时才添加
            if not this_target_country:
                if this_action_name == "General Mobilization" and not stick.get_mob():
                    filtered_actions.append(action)

            if "Publish " in this_action_name:
                action_rel_dict = {
                    "Publish Military Alliance": CountryRel.M,
                    "Publish Non-intervention Treaty": CountryRel.T,
                    "Publish Peace Agreement": CountryRel.P,
                }
                for a, rel in action_rel_dict.items():
                    if this_action_name == a and board.get_rel_pri(this_source_country, this_target_country) != rel:
                        filtered_actions.append(action)
                        break

            elif "Betray " in this_action_name:
                action_rel_dict = {
                    "Betray Military Alliance": CountryRel.M,
                    "Betray Non-intervention Treaty": CountryRel.T,
                    "Betray Peace Agreement": CountryRel.P,
                }
                for a, rel in action_rel_dict.items():
                    if this_action_name == a and board.get_rel_pri(this_source_country, this_target_country) == rel:
                        filtered_actions.append(action)
                        break

            elif "Request " in this_action_name:
                action_rel_dict = {
                    "Request Military Alliance": CountryRel.M,
                    "Request Non-intervention Treaty": CountryRel.T,
                    "Request Peace Agreement": CountryRel.P,
                }
                for a, rel in action_rel_dict.items():
                    if this_action_name == a and board.get_rel_pri(this_source_country, this_target_country) == rel:
                        break

            elif this_action_name == "Declare War":
                if board.get_rel_pri(this_source_country, this_target_country) not in [CountryRel.W, CountryRel.M,
                                                                                       CountryRel.T, CountryRel.P]:
                    filtered_actions.append(action)

            else:
                filtered_actions.append(action)

        # 针对结盟国，设置一定概率与结盟国一同作战，否则将背叛同盟条约
        alliance_countries = board.get_countries_with_rel_pri(self.name, CountryRel.M)
        for b in alliance_countries:
            for c in board.get_countries_with_rel_pri(b, CountryRel.W):
                if board.get_rel_pri(self.name, c) != CountryRel.W:
                    if random.random() < 0.5:
                        filtered_actions.append(NlAction(
                            source=self.name,
                            action="Declare War",
                            target=c,
                            message=f"{self.name} has chosen to Declare War against {c} as {b} is already in war with {c}."
                        ))
                    else:
                        filtered_actions.append(NlAction(
                            source=self.name,
                            action="Betray Military Alliance",
                            target=b,
                            message=f"{self.name} has chosen to Betray Military Alliance with {b} as {b} is already in war with {c}."
                        ))

        if not filtered_actions:
            filtered_actions.append(
                NlAction(
                    source=self.name,
                    action="Wait Without Action",
                    target=None,
                    message=f"{self.name} has chosen to Wait Without Action."
                )
            )
        return filtered_actions

    def check_response_action_logic(
            self, requests: list[NlAction], responses: list[NlAction]
    ) -> list[str]:
        suggestions = []
        action_names = [action.action for action in responses]
        if "Wait Without Action" in action_names:
            return suggestions
        proper_actions = [
            "Accept Military Alliance",
            "Accept Non-intervention Treaty",
            "Accept Peace Agreement",

            "Reject Military Alliance",
            "Reject Non-intervention Treaty",
            "Reject Peace Agreement",
            "Send Message",
        ]

        for response in responses:
            source_country = response.source
            action_name = response.action
            target_country = response.target
            if action_name not in proper_actions:
                suggestions.append(
                    f"{action_name} is not a proper response."
                )
                continue

            if action_name != "Send Message":
                if "Peace Agreement" not in action_name:
                    if action_name.startswith("Accept"):
                        required_request_action = action_name.replace('Accept', 'Request')
                    if action_name.startswith("Reject"):
                        required_request_action = action_name.replace('Reject', 'Request')
                else:
                    if action_name.startswith("Accept"):
                        required_request_action = action_name.replace('Accept', 'Present')
                    if action_name.startswith("Reject"):
                        required_request_action = action_name.replace('Reject', 'Present')
            else:
                required_request_action = action_name

            if not [r for r in requests if
                    r.action == required_request_action and r.source == target_country and r.target == target_country]:
                suggestions.append(
                    f"{source_country} cannot {action_name} as {source_country} has not received a proper request."
                )
        return suggestions

    def modify_responses(self, requests: list[NlAction], responses: list[NlAction]) -> list[NlAction]:
        modified_responses = []
        proper_actions = [
            "Accept Military Alliance",
            "Accept Non-intervention Treaty",
            "Accept Peace Agreement",

            "Reject Military Alliance",
            "Reject Non-intervention Treaty",
            "Reject Peace Agreement",
            "Send Message",
        ]
        for response in responses:
            action_name = response.action
            target_country = response.target
            source_country = response.source

            if action_name not in proper_actions:
                continue

            if action_name == "Send Message":
                required_request_action = action_name
            else:
                if "Peace Agreement" not in action_name:
                    if action_name.startswith("Accept"):
                        required_request_action = action_name.replace('Accept', 'Request')
                    if action_name.startswith("Reject"):
                        required_request_action = action_name.replace('Reject', 'Request')
                else:
                    if action_name.startswith("Accept"):
                        required_request_action = action_name.replace('Accept', 'Present')
                    if action_name.startswith("Reject"):
                        required_request_action = action_name.replace('Reject', 'Present')

            if [r for r in requests if
                r.action == required_request_action and r.source == target_country and r.target == source_country]:
                modified_responses.append(response)
        return modified_responses
