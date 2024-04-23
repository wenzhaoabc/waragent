# -*- coding: utf-8 -*-
import pydantic
from src.history.agent_actions import Action, ActionType, ActionInputType
from src.history.profile import CountryProfile

class NlAction(pydantic.BaseModel):
    source: str
    action: str
    target: str
    message: str


class Formatter:
    """
    This class is used to format the data in the neural language.
    将结构化的数据转为自然语言
    """

    def __init__(self, data):
        self.data = data

    def format(self):
        return self.data

    def actions_format(
        self, source_country: CountryProfile, actions: list[Action]
    ) -> list[NlAction]:
        """
        格式化动作列表
        Args:
            source_country: 动作来源国家
            actions: 动作列表
        Returns:
            list[dict]: 格式化后的动作列表, {"source": str, "action": str, "target": str, "message": str}
        """
        actions.sort(key=lambda x: x.action_type.input_type)

        final_messages = []
        source_country_name = source_country.country_name

        for a in actions:
            action_type = a.action_type
            action_name = action_type.name
            action_input = a.action_input
            action_input_type = action_type.input_type

            if action_input_type == ActionInputType.empty:
                final_messages.append(
                    {
                        "source": source_country_name,
                        "action": action_name,
                        "target": "",
                        "message": "",
                    }
                )
            elif action_input_type == ActionInputType.country_list:
                for target in action_input:
                    final_messages.append(
                        {
                            "source": source_country.country_name,
                            "action": action_name,
                            "target": target,
                            "message": f"{source_country_name} has chonse to {action_name} to {target}.",
                        }
                    )
            elif action_input_type == ActionInputType.country_dict:
                """No such action in the current version."""
                pass
            elif action_input_type == ActionInputType.country_list_dict:
                for target, properties in action_input.items():
                    final_messages.append(
                        {
                            "source": source_country_name,
                            "action": action_name,
                            "target": target,
                            "message": f"{source_country_name} has chosen to {action_name} to {target}, and the content is {properties["content"]}",
                        }
                    )

        return final_messages
