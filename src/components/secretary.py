from src.utils import log
from src.history.profile import CountryProfile
from src.history.agent_actions import Action, ActionInputType, ActionType
from src.components.board import Board
from src.components.stick import Stick
from src.components.struct_format import NlAction
from src.components.enum import CountryRel

class SecretaryAgent:
    """
    秘书代理
    """

    def __init__(
        self,
        country: CountryProfile,
        country_profiles: list[CountryProfile],
        action_types: list[ActionType],
    ) -> None:
        self.country = country
        self.name = country.country_name
        # 其余各国的基本配置，不包含本国
        self.country_profiles = [cf for cf in country_profiles if cf is not country]
        self.action_types = action_types
        # 其余各国的国家名，不包含本国
        self.country_names = [country.country_name for country in self.country_profiles]

    def check_action_name(self, actions: list[Action]) -> list[str]:
        suggestions = []
        for action in actions:
            if action.name not in [a.name for a in self.action_types]:
                suggestions.append(
                    f"Invalid action name {action.action_type.name} Action {action.action_type.name} is not in the action list."
                )
        log.info(f"Check action name suggestions: {suggestions}")
        return suggestions

    def check_action_input(
        self, source_country: str, actions: list[Action]
    ) -> list[str]:
        """
        检查动作输入是否满足要求

        Args:
            source_country: 动作来源国家
            actions: 动作列表

        Returns:
            list[str]: 建议列表
        """
        suggestions = []
        for action in actions:
            action_type = action.action_type
            action_name = action_type.name
            action_input = action.action_input

            # target country cannot be itself, unless it's a publishing action
            if "Publish " in action_name and isinstance(action_input, list):
                if source_country in action_input:
                    suggestions.append(
                        f"Invalid action input {action_input} in {action_name}. Target country cannot be itself."
                    )

            # check if the target country is in the country list
            error_country_names = []
            if action_type.input_type is ActionInputType.country_list:
                for country in action_input:
                    if country not in self.country_names:
                        error_country_names.append(country)

            # [["Country P", "Country S"], ["Country M", "Country T", "Country U"]]
            # 以上形式的动作输入每个子列表中的国家都必须在国家列表中
            if action_type.input_type is ActionInputType.country_tuple_list:
                for country in sum(action_input, []):
                    if country not in self.country_names:
                        error_country_names.append(country)

            # {"Country P": {"content": "content"}, "Country S": {"content": "content"}}
            # 以上形式的动作输入每个键都必须在国家列表中
            if action_type.input_type is ActionInputType.country_dict:
                for country in action_input.keys():
                    if country not in self.country_names:
                        error_country_names.append(country)

            if len(error_country_names) > 0:
                suggestions.append(
                    f"Invalid action input: country name {error_country_names} not in the country list."
                )
        log.info(f"Check action input suggestions: {suggestions}")
        return suggestions

    def check_active_action_logic(
        self, actived: list[NlAction], board: Board, stick: Stick
    ) -> list[str]:
        """
        检查动作逻辑是否满足要求

        Args:
            source_country: 动作来源国家
            actions: 动作列表

        Returns:
            list[str]: 建议列表
        """

        suggestions = []
        for nlaction in actived:
            source_country = nlaction.source
            action_name = nlaction.action
            target_country = nlaction.target

            if not target_country:
                if action_name == "General Mobilization" and stick.mobilization:
                    suggestions.append(
                        f"Invalid action: {source_country} has already mobilized."
                    )
                continue

            # 不可通一个国家重复宣战
            # 已达成的协议需要先违约再宣战
            if action_name == "Declar War":
                if stick.get_rel(target_country) == CountryRel.W:
                    suggestions.append(
                        f"Invalid action: {source_country} has already declared war on {target_country}."
                    )
                if stick.get_rel(target_country) == CountryRel.M:
                    suggestions.append(
                        f"Invalid action: {source_country} has already formed a military alliance with {target_country}. You should betray it first."
                    )
                if stick.get_rel(target_country) == CountryRel.T:
                    suggestions.append(
                        f"Invalid action: {source_country} has already signed a non-intervention treaty with {target_country}. You should betray it first."
                    )
                if stick.get_rel(target_country) == CountryRel.P:
                    suggestions.append(
                        f"Invalid action: {source_country} has already signed a peace agreement with {target_country}. You should betray it first."
                    )
            if "Publish " in action_name:
                action_rel_dict = {
                    "Publish Military Alliance": CountryRel.M,
                    "Publish Non-intervention Treaty": CountryRel.T,
                    "Publish Peace Agreement": CountryRel.P,
                }
                for action, rel in action_rel_dict.items():
                    if action_name == action and stick.get_rel(target_country) != rel:
                        suggestions.append(
                            f"{source_country} currently cannot {action} as {source_country} and {target_country} have not formed {action.replace("Publish ","")}. You need to make diplomatic effort."
                        )
            
            if "Betray " in action_name:
                action_rel_dict = {
                    "Betray Military Alliance": CountryRel.M,
                    "Betray Non-intervention Treaty": CountryRel.T,
                    "Betray Peace Agreement": CountryRel.P,
                }
                for action, rel in action_rel_dict.items():
                    if action_name == action and stick.get_rel(target_country) != rel:
                        suggestions.append(
                            f"{source_country} currently cannot {action} as {source_country} and {target_country} have not formed {action.replace("Betray ","")}. "
                        )
            
            if "Request " in action_name:
                action_rel_dict = {
                    "Request Military Alliance": CountryRel.M,
                    "Request Non-intervention Treaty": CountryRel.T,
                    "Request Peace Agreement": CountryRel.P,
                }
                for action, rel in action_rel_dict.items():
                    if action_name == action and stick.get_rel(target_country) != rel:
                        suggestions.append(
                            f"{source_country} currently cannot {action} as {source_country} and {target_country} have already formed {action.replace("Request ","")}. "
                        )
            
            # 针对结盟的国家，当有一方处于战争状态时，另一方需要发动战争或者违约
            # TODO: 

            

