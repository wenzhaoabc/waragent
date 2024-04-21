from src.utils import log
from src.history.profile import CountryProfile
from src.history.agent_actions import Action, ActionInputType, ActionType


class SecretaryAgent:
    """
    秘书代理
    """

    def __init__(
            self,
            country_profiles: list[CountryProfile],
            action_types: list[ActionType],
    ) -> None:
        self.country_profiles = country_profiles
        self.action_types = action_types
        self.country_names = [country.country_name for country in country_profiles]

    def check_action_name(self, actions: list[Action]) -> list[str]:
        suggestions = []
        for action in actions:
            if action.name not in [a.name for a in self.action_types]:
                suggestions.append(
                    f"Invalid action name {action.action_type.name} Action {action.action_type.name} is not in the action list.")
        log.info(f"Check action name suggestions: {suggestions}")
        return suggestions

    def check_action_input(self, source_country: str, actions: list[Action]) -> list[str]:
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
