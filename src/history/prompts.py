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
{format_suggestion}
"""


def p_first_action_instruction_with_format(
    error_action: str, format_suggestion: list[str]
) -> str:
    """首次动作生成的指导提示"""
    return f"""{p_first_action_instruction()}
{p_action_format_check("", format_suggestion)}
"""


def p_situation(situation: str) -> str:
    """
    prompt: generate
    situation
    prompt
    :param
    situation: The
    current
    situation
    """
    return f"""
    The
    current
    situation is: \n
    {situation}
    """
