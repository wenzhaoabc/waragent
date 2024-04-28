# -*- coding:utf-8 -*-
"""
Copy right:
Action checker prompt
author: wenzhaoabc
Date: 2024-04-28
"""


def p_format_check(
        error_actions: str, suggestions: list[str]
) -> str:
    """动作格式错误，指导再次生成"""
    return f"Previously, you have made actions with invalid names or input formats:\n" \
           f"{error_actions} \n" \
           f"Please generate the action list again according to the below suggestions:\n" \
           f"{'\n'.join(suggestions)}"


def p_logic_check(
        error_actions: str, suggestions: list[str]
) -> str:
    return f"A secretary has checked your previously proposed actions : {error_actions}\n" \
           f"The current action and preceding actions fail to meet the logical criteria for each action, " \
           f"and the secretary disagrees with the action list for the following reasons. Please try again.\n" \
           f"{'\n'.join(suggestions)}"
