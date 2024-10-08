# -*- coding: utf-8 -*-
import json
from json import JSONDecodeError

import pydantic
from collections import defaultdict
from src.profiles.agent_actions import Action, ActionInputType
from src.utils import log


class NlAction(pydantic.BaseModel):
    source: str
    action: str
    target: str | None
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
            self, source_country: str, actions: list[Action]
    ) -> list[NlAction]:
        """
        格式化动作列表
        Args:
            source_country: 动作来源国家
            actions: 动作列表
        Returns:
            list[dict]: 格式化后的动作列表, {"source": str, "action": str, "target": str, "message": str}
        """
        actions.sort(key=lambda x: x.action_type.input_type.value)

        final_messages = []
        source_country_name = source_country

        for a in actions:
            action_type = a.action_type
            action_name = action_type.name
            action_input = a.action_input
            action_input_type = action_type.input_type

            if action_input_type == ActionInputType.empty:
                m = NlAction(
                    source=source_country_name,
                    action=action_name,
                    target="",
                    message=f"{source_country_name} has chosen to {action_name}.",
                )
                final_messages.append(m)
            elif action_input_type == ActionInputType.country_list:
                for target in action_input:
                    m = NlAction(
                        source=source_country_name,
                        action=action_name,
                        target=target,
                        message=f"{source_country_name} has chosen to {action_name} to {target}.",
                    )
                    final_messages.append(m)
            elif action_input_type == ActionInputType.country_tuple_list:
                """No such action in the current version."""
                pass
            elif action_input_type == ActionInputType.country_dict:
                for target, properties in action_input.items():
                    if isinstance(properties, str):
                        try:
                            properties = json.loads(properties)
                        except JSONDecodeError as e:
                            properties = {"content": properties}
                            log.info(f"JSON decoding error:{e} - properties = {properties}")
                    m = NlAction(
                        source=source_country_name,
                        action=action_name,
                        target=target,
                        message=f"{source_country_name} has chosen to {action_name} to {target}, and the content is {properties['content']}",
                    )
                    final_messages.append(m)

        return final_messages

    def actions_to_json(
            self, new_actions: list[Action], response_actions: list[Action] | None = None
    ) -> str:
        """将国家代理的动作转为符合格式要求的JSON"""
        new_action_dict = {}
        if new_actions:
            new_actions.sort(key=lambda x: x.action_type.input_type.value)
            for na in new_actions:
                new_action_dict[na.action_type.name] = na.action_input

        response_actions_dict = {}
        if response_actions:
            response_actions.sort(key=lambda x: x.action_type.input_type.value)
            for ra in response_actions:
                response_actions_dict[ra.action_type.name] = ra.action_input

        if response_actions_dict:
            return json.dumps(
                {
                    "response_actions": response_actions_dict,
                    "new_actions": new_action_dict,
                }
            )
        else:
            return json.dumps(new_action_dict)

    def nlaction_str(self, nl_actions: list[NlAction]) -> str:
        nl_actions = sorted(nl_actions, key=lambda x: x.source)
        if len(nl_actions) == 0:
            return ""
        source_country_name = nl_actions[0].source
        nl_actions = filter(lambda x: x.source == source_country_name, nl_actions)
        clusters = defaultdict(list)
        for action in nl_actions:
            clusters[action.action].append(action.target)
        res = dict(clusters)
        return json.dumps(res)

    def actions_to_nl(self, new_actions: list[NlAction], response_actions: list[NlAction] | None = None):
        res = {}
        for na in response_actions + new_actions:
            s = na.source
            t = na.target
            a = na.action
            m = na.message
            if a not in res.keys():
                if a == "Send Message":
                    res[a] = [m.replace(s, "We")]
                else:
                    res[a] = [t]
            else:
                if a == "Send Message":
                    res[a].append(m.replace(s, "We"))
                else:
                    res[a].append(t)

        str_res = {}
        for a, cs in res.items():
            if a == "Send Message":
                str_res[a] = " ".join(cs)
            else:
                ts = ''.join([i if i else '' for i in cs])
                str_res[a] = f"We will {a}{' to ' if len(ts) > 1 else ' '}{ts}."

        return str_res

# n = NlAction(source="S", action="A", target="T", message="M")
