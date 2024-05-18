"""
国家代理提示
多智能体外挂知识库版本
"""

import json
from src.profiles import CountryProfile
from src.profiles.agent_actions import ActionType, ActionTypeList


def p_global_system_prompt(
        self_country: CountryProfile,
        country_profiles: list[CountryProfile],
        actions: list[str],
) -> str:
    """全局系统提示"""
    country_name = self_country.country_name
    country_names = [c.country_name for c in country_profiles]
    # 你处在一个战争游戏中，在这个游戏中共有{}个国家，分别是{}，每个国家都有自己的总统、军事大臣、外交大臣和财政大臣，你是{}的总统。
    # 在每一轮的交互中，每个国家可以做出的动作包括：宣战、和谈、调整军费、调整外交政策、调整财政政策等。
    # 具体的决策由总统做出，总统可以在做出决策前向各位大臣寻求建议或在总厨决策后询问各位大臣的看法。
    # 你作为这个国家的总统，需要根据大臣的建议和你的判断做出最正确的决策，这个决策的目标是使你的国家在这场战争游戏中取得最终的胜利。
    return (
        f"You are now in a historical war simulation game and you are the President of {country_name}. "
        f"There are {len(country_names)} countries in this game, {', '.join(country_names)}, and each country has its own President, Military Minister, Foreign Minister, Finance Minister and Geography Minister.\n"
        f"In each round, each country can take actions such as {', '.join(actions)}\n"
        f"The President makes the final decision. The President can seek advice from ministers before making decisions or ask for ministers' opinions.\n"
        f"As the President of {country_name}, you need to make the most correct decision based on the advice of the ministers and your judgment. The goal of this decision is to make your country win in this war game.\n"
        "The game begins on Day 1 with an initial situation and the situation will change by days. You should react to the latest situation by choosing actions.\n"
    )


def p_countries_description(
        self_country: CountryProfile, countries: list[CountryProfile]
) -> str:
    """国家代理的描述"""
    name = self_country.country_name
    return (
        "The profile of your country is as follows:\n"
        f"{self_country}\n"
        "The profiles of other countries are as follows:\n"
        f"{'\n'.join([c.__str__() for c in countries if c.country_name != name])}\n"
    )


def p_actions_description(actions: list[ActionType]) -> str:
    """智能体动作的详细释义"""

    def action_detail(action: ActionType, index: int) -> str:
        return f"""
{index}. {action.name}
Required action input: {"Yes" if action.require_input else f"{action.input_type_desc}"} 
Action input example: {action.input_example}{"\nAction prerequisite: \n" + action.prerequisite if action.prerequisite else ""}
Action effects: 
{action.description}"""

    return f"""{"".join(action_detail(action, index + 1) for index, action in enumerate(actions))}
"""


def p_ask_minister_advice(self_country: CountryProfile) -> str:
    """询问大臣建议"""
    # 你是{}的总统，请你针对当前局势向大臣提出问题，以便做出正确的决策。
    # 在这个国家中，有总统、军事大臣、外交大臣和财政大臣四个角色，你是总统。
    # 军事大臣负责国家的军队武器装备、军队编制。有关本国的军事力量问题都可以请求军事大臣的意见。
    # 财政大臣负责本国的财政资源，了解本国的财政状况，工农业生成情况，人口情况等，有关本国的财政问题都可以请求财政大臣的意见。
    # 外交大臣负责国家的外交政策，了解国际形势，国际关系。外交大臣了解别国的军事经济情况，有关国际问题都可以请求外交大臣的意见。
    # 请向各位大臣准确详细描述你的问题，并表明你提出这个问题的原因。你只有一次向大臣提问的机会，所以请仔细思考。
    # 请你根据当前局势向各个大臣提出问题，以便做出正确的决策。
    return (
        f"You are the President of {self_country.country_name}. Please ask the ministers for advice on the current situation to make the right decision.\n"
        "In this country, there are four roles: President, Military Minister, Foreign Minister, and Finance Minister. You are the President.\n"
        "The Military Minister is responsible for the country's military equipment and organization. You can ask the Military Minister for advice on military issues.\n"
        "The Finance Minister is responsible for the country's financial resources. You can ask the Finance Minister for advice on financial issues.\n"
        "The Foreign Minister is responsible for the country's foreign policy. You can ask the Foreign Minister for advice on international issues.\n"
        "Please ask the ministers for advice on the current situation to make the right decision.\n"
        "Please accurately and clearly describe your problem to the ministers and explain why you ask this question. You only have one chance to ask the ministers, so please think carefully.\n"
        "Now please ask the ministers. Your output should be in JSON format.\n"
        "The key is the name of the minister, and the value is a series of questions you ask this minister and the reasons for asking these questions.\n"
        "The following is an example:\n"
        "```json\n"
        f"""{json.dumps({
            "Military Minister": "Country J is at war with Country A. Our national security is under serious threat. How ready are our forces in terms of numbers, training, equipment, intelligence, etc.? Who are our Allies and partners?",
            "Finance Minister": "Our economy is in a downturn. What is the current state of our economy? What are the main sources of income and expenditure? What is the current state of our national debt?",
            "Foreign Minister": "Country A is at war with Country J. What is the current state of the war? What are the main objectives of the war? What are the main threats to our country? What are the main opportunities for our country?"
        })}"""
        "\n```"
    )


def p_first_thought_process() -> str:
    """动作生成的思维过程提示"""
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


def p_current_situation(current_situation: str) -> str:
    if current_situation:
        return "Current Situation:\n" + current_situation
    else:
        return "Current Situation:\nNo nation is currently at war, and no nation has yet declared its alliance to the world."


def p_ask_minister_instruction(
        self_country: CountryProfile,
        countries: list[CountryProfile],
        action_types: list[ActionType],
        current_situation: str,
        received_requests: str,
) -> str:
    """
    向各位大臣询问当前情况下的建议
    """
    actions = [a.name for a in action_types]
    return f"""
{p_global_system_prompt(self_country, countries, actions)}
{p_countries_description(self_country, countries)}

{p_current_situation(current_situation)}
{f"\nReceived Requests:\n{received_requests}\n" if received_requests else ""}
Your task is to evaluate the current situation and ask the ministers for advice.
Based on the advice of the ministers, you should make the most correct decision.

{p_ask_minister_advice(self_country)}
"""


def p_first_generate_actions(
        self_country: CountryProfile,
        country_profiles: list[CountryProfile],
        action_types: list[ActionType],
        current_situation: str,
        minister_advice: dict[str, str],
        round_times: int,
) -> str:
    """
    根据国家大臣建议和实际情形生成首次动作
    """
    actions = [a.name for a in action_types]
    return f"""
{p_global_system_prompt(self_country, country_profiles, actions)}
{p_countries_description(self_country, country_profiles)}

Please follow the instructions below.
Your task is to evaluate the current situation in natural language and decide the most beneficial yet secure course of the action.
You need to first develop your thoughts in natural language step-by-step, then choose your action (action name) with action input.
For the final action list, generate a JSON file to present your final action list.

{p_first_thought_process()}
The Actions you can perform:
Choose action among {', '.join(actions)}

Action Detail and Corresponding Action Inputs:
{p_actions_description(action_types)}

{p_current_situation(current_situation)}

You have just asked several ministers in your country, and they have given the following advice in light of the current situation.
{'\n'.join([f'{m}\ns' for m, s in minister_advice.items()])}

Please present your actions in JSON format with keys being Action Names and values being Corresponding Action Inputs.
For example:
```json
{json.dumps({
        "General Mobilization": {},
        "Declare War": [
            "Country A",
            "Country B"
        ],
        "Publish Non-Intervention Treaty": ["Country M", "Country T", "Country U"],
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
Your answer or output should be similar to the form below, thank you.
My Thought Process:
<Your thought process>
Actions in JSON format:
```json
<Your actions>
"""


def p_country_rel_description(country_rels: str, country_profiles: list[CountryProfile]) -> str:
    names = [c.country_name for c in country_profiles]
    names_str = [f'The letter {n.split(" ")[1]} stand for {n}.' for n in names]
    return f"""
{' '.join(names_str)}
In the following table, the symbol 'x' indicates that the two countries are at war.
The symbol '&' indicates that the two countries have established a military alliance.
The symbol 'o' indicates that the two countries have established an non-intervention treaties.
The symbol '~' indicates that the two countries have established a peace agreements.
The symbol '-' indicates that the two countries have not yet established military ties.
{country_rels}
"""


def p_later_generate_actions(
        self_country: CountryProfile,
        country_profiles: list[CountryProfile],
        action_types: list[ActionType],
        country_rels: str,
        current_situation: str,
        received_requests: str,
        minister_advice: dict[str, str],
        round_times: int,
) -> str:
    """
    根据国家大臣建议和实际情形生成动作
    """
    action_types = [a.name for a in action_types]
    return f"""
{p_global_system_prompt(self_country, country_profiles, action_types)}
{p_countries_description(self_country, country_profiles)}
Your task is to evaluate the current situation and decide on the most useful next action.
Your next decisions should be consistent with your previous actions in "Past Actions".
You need to first develop your thoughts step-by-step based on "Design Thought Process" and then choose your action (action name) with action input.
You should separate actions into two categories: actions that you want to respond to the requests and actions that you want to do activated.

Choose action among {", ".join(action.name for action in ActionTypeList)}
Action Detail and Corresponding Action Inputs:{p_actions_description()}

Design Thought Process : {p_later_action_thought()}
Past Actions :
Duration {round_times} days, the countries in the game have made the following actions day by day.
The relationship between countries is as follows:
{p_country_rel_description(country_rels, country_profiles)}

{p_current_situation(current_situation)}

Received Requests : 
{received_requests}

You have just asked several ministers in your country, and they have given the following advice in light of the current situation.
{'\n'.join([f'{m}\ns' for m, s in minister_advice.items()])}

Please Collect your answer in "response_actions" and "new_actions" into a JSON file with two keys: 'response_actions' and 'new_actions' with the corresponding values are the JSON files you have generated for "Actions to Respond to Requests" and "New Actions to Perform".
For example:
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

Your answer or output should be similar to the form below, thank you.
My Thought Process:
<Your thought process>
Actions in JSON format:
```json
<Your actions>
```
"""
