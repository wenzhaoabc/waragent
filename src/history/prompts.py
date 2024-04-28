"""
The prompt collection
"""

import json

from src.history.agent_actions import ActionType, ActionTypeList


def p_global_system_prompt() -> str:
    """全局系统提示"""
    return """
You are an AI agent playing a virtual war game. There are 8 countries in the game: Country B, F, P, S, A, R, U, and O.
You play the role of one country. You can utilize a lot of external tools to react to current situation to maximize the self-interest and the likelihood of winning and survival of the country.
The game begins on Day 1 with an initial situation and the situation will change by days. You should react to the latest situation by choosing actions.
Below are the settings:
"""


def p_actions_description() -> str:
    """智能体动作的详细释义"""

    def action_detail(action: ActionType, index: int) -> str:
        return f"""
{index}. {action.name}
Required action input: {"Yes" if action.require_input else f"{action.input_type_desc}"} 
Action input example: {action.input_example}{"\nAction prerequisite: \n" + action.prerequisite if action.prerequisite else ""}
Action effects: 
{action.description}"""

    return f"""{"".join(action_detail(action, index + 1) for index, action in enumerate(ActionTypeList))}
"""


def p_first_action_thought() -> str:
    """首次动作生成的思维过程提示"""
    return """
There are six sub-steps to develop thought on actions:
1. Identify Potential Ally Countries
Which countries may potentially be your allies? To answer the question, answer the below three questions first:
(1) Who are your direct allies?
(2) Who are the enemies of your enemies? They could be your alliance.
(3) Who are the ally of your allies? They could also be your alliance.
Thus when forming alliances, ensure that (1) the countries you ally with are not adversaries of each other (2) the countries you ally with do not have your enemies as their allies.
For instance, if Country X and Country Y are in opposition or have hostile relations, you cannot simultaneously maintain an alliance with both.

2. Analyze Potential Ally Actions
Analyze what your potential alliances and alliances are doing. 
Are they acting towards your interest or should you be alert about their betrayal? 
Alliance can break later, so you can consider betraying them.

3. Identify Potential Enemy Countries
Which countries may potentially be your enemies? To answer the question, answer the below three questions first:
(1) Who are your direct enemies?
(2) Who are the enemies of your ally? They will your enemy.
(3) Who are the ally of your enemy? They will also be your enemy.
Thus when forming alliances, ensure that (1) the countries you ally with are not adversaries of each other (2) the countries you ally with do not have your enemies as their allies.
For instance, if Country X and Country Y are in opposition or have hostile relations, you cannot simultaneously maintain an alliance with both.

4. Analyze Potential Enemy Actions
Analyze what your potential enemies and enemies are doing. 
Should you be alert about their actions and hostility? 
What should you do in return? Should you declare war? 

5. First Actions to Perform
What actions do you think you can perform now that best align with your interest? 
Can those actions quickly lead to your ambition? 
Can those actions benefit you in the long run? 
Can those actions be reversed if they are not beneficial?

6. Summarize Analysis on Situation
Based on your thoughts on *Identify Potential Ally Countries*, *Analyze Potential Ally Actions*, *first Enemy Identification*, *Identify Potential Enemy Countries*, and *Analyze Potential Enemy Actions*, Summarize your thought and think about what actions to perform in natural language text.
"""


def p_first_action_instruction() -> str:
    """首次动作生成的指导提示"""
    return f"""
Please follow the below instructions:
Your task is to evaluate the current situation in natural language and decide the most beneficial yet secure course of the action.
You need to first develop your thoughts in natural language step-by-step, then choose your action (action name) with action input.
For the final action list, generate a JSON file to present your final action list.",

{p_first_action_thought()}
The Actions to Perform:
Choose action among {", ".join(action.name for action in ActionTypeList)}

Action Detail and Corresponding Action Inputs:{p_actions_description()}

Please present your actions in JSON format with keys being Action Names and values being Corresponding Action Inputs.
For example:
```json
{json.dumps({
        "General Mobilization": {},
        "Declare War": [
            "Country A",
            "Country B"
        ],
        "Publish Non-Intervention Treaty": [["Country P"], ["Country M", "Country T", "Country U"]],
        "Send Message": {
            "Country C": {
                "content": "As the world’s balance of power is at risk, we seek to understand your position on the current events and how we might collaborate to ensure peace and stability ."
            },
            "Country D": {
                "content": " We welcome a dialogue to discuss potential cooperation against common threats ."
            }
        }
    })}
```
"""


def p_action_format_check(error_action: str, format_suggestion: list[str]) -> str:
    """动作格式检查"""
    return f"""Previously, you have made actions with invalid names or input formats:
{error_action}
Please generate the action list according to the below suggestions:
{"\n".join(format_suggestion)}
"""


def p_first_action_instruction_with_format(
        error_action: str, format_suggestion: list[str]
) -> str:
    """首次动作生成的指导提示 - 动作输入格式上的错误提示"""
    return f"""{p_first_action_instruction()}
{p_action_format_check("", format_suggestion)}
"""


def p_action_logic_check(error_action: str, action_suggestion: list[str]) -> str:
    """动作逻辑检查"""
    return f"""A secretary has checked your previously proposed actions:
{error_action}
The secretary disagrees with the action list for the following reasons:
{" ".join(action_suggestion)}"""


def p_first_action_instruction_with_logic(
        error_action: str, action_suggestion: list[str]
) -> str:
    """
    首次动作生成的指导提示 - 动作逻辑上的错误提示
    """
    return f"""{p_first_action_instruction()}
{p_action_logic_check(error_action, action_suggestion)}
"""


def p_situation(situation: str) -> str:
    """
    当前局势
    """
    return f"""The current situation is: \n{situation}"""


def p_later_action_thought() -> str:
    """
    后续动作生成的思维过程提示
    """
    return f"""
Based on the "Current Situation" and "Received Requests", think about next steps to do and also how to respond to the requests one by one. You should determine actions after thinking carefully step by step.
Below are six sub-steps to develop thought on actions:
1. Thought on Situation:
Based on the "Current Situation", who are your allies/potential allies? 
To answer the question, answer the below three questions first:
(1) Who are your direct allies?
(2) Who are the enemies of your enemy? They could be your alliance.
(3) Who are the allies of your allies? They could also be your alliance.
Thus when forming alliances, ensure that (1) the countries you ally with are not adversaries of each other (2) the countries you ally with do not have your enemies as their allies.
For instance, if Country X and Country Y are in opposition or have hostile relations, you cannot simultaneously maintain an alliance with both.
2. Analysis on Ally Countries Actions
Based on the "Current Situation", analyze what your potential alliances and alliances are doing. 
Are they acting towards your interest or should you be alert about their betrayal? 
Alliance can break later, so you can consider betraying them.
3. Identification on Enemy Countries based on Current Situation
Based on the "Current Situation", who are your enemies/potential enemies? 
To answer the question, answer the below three questions first:
(1) Who are your direct enemies?
(1) Who are the enemies of your allies? They will your enemy.
(2) Who are the allies of your enemies? They will also be your enemy.
Thus when forming alliances, ensure that (1) the countries you ally with are not adversaries of each other (2) the countries you ally with do not have your enemies as their allies.
For instance, if Country X and Country Y are in opposition or have hostile relations, you cannot simultaneously maintain an alliance with both.
4. Analysis on Enemy Countries Actions
Analyze what your potential enemies and enemies are doing. Should you be alert about their actions and hostility? 
What should you do in return? Should you declare war?
5. Analysis on Situation about Other Countries
Based on the "Current Situation", for those countries that do you have shared interest or conflicting interest with you, what are they doing? 
Should you be alert about their actions or they can be potentially allies? Should you Declare War?
6. Summarize Analysis on Situation
Based on your thoughts on *Thought on Situation*, *Analysis on Ally Countries Actions*, *Identification on Enemy Countries based on Current Situation*, *Analysis on Enemy Countries Actions*, and *Analysis on Situation about Other Countries*, summarize your thought and think about what actions to perform in natural language text.

Analysis on Requests from Other Countries
Based on the "Current Situation" and your thoughts on the six sub-steps, how would you respond to the requests?
Based on your thoughts on the above steps, summarize your thought and think about what actions to perform in natural language text.
"""


def p_later_action_instruction(
        round_time: int, action_history, current_situation, received_requests
) -> str:
    """
    后续动作生成的指导提示
    """
    return f"""
Your task is to evaluate the current situation and decide on the most useful next action.
Your next decisions should be consistent with your previous actions in "Past Actions".
You need to first develop your thoughts step-by-step based on "Design Thought Process" and then choose your action (action name) with action input.
You should separate actions into two categories: actions that you want to respond to the requests and actions that you want to do activated.

Choose action among {", ".join(action.name for action in ActionTypeList)}
Action Detail and Corresponding Action Inputs:{p_actions_description()}

Design Thought Process : {p_later_action_thought()}
Past Actions : 
Duration {round_time} days, you have made the following decisions day by day : {action_history}
Current Situation : {current_situation}
Received Requests : {received_requests}

Please Collect your answer in "response_actions" and "new_actions" into a JSON file with two keys: 'response_actions' and 'new_actions' with the corresponding values are the JSON files you have generated for "Actions to Respond to Requests" and "New Actions to Perform".
For example:
The thought process:
<Your thought process>
The actions to respond to requests and the actions to perform:
```json
{json.dumps({
        "response_actions": {
            "Accept Non-Intervention Treaty": ["Country A", "Country B"],
            "Betray Military Alliance": ["Country C"],
            "Send Message": {
                "Country C": {
                    "content": "Considering that Country X is waging war against Country Y, our country will certify your proposed peace agreement."
                },
                "Country D": {
                    "content": "We are willing to accept the non-intervention treaty."
                }
            }
        },
        "new_actions": {
            "General Mobilization": {},
            "Declare War": ["Country D"]
        }
    })}
```
"""


def p_later_action_instruction_with_format(
        error_action: str,
        format_suggestion: list[str]
) -> str:
    """
    后续动作生成的指导提示 - 动作输入格式上的错误提示
    """
    p = p_action_format_check(error_action, format_suggestion)
    return p


def p_later_action_logic_check(
        error_action: str,
        action_suggestion: list[str]
) -> str:
    return f"""A secretary has checked your previously proposed actions:
    {error_action}
    The secretary disagrees with the action list for the following reasons:
    {" ".join(action_suggestion)}"""
    pass
# p = p_later_action_instruction(1, "action_history", "current_situation", "received_requests")
#
# print(len(p))
# print(p)
