import re
from typing import Any


def extract_json(input_text: str) -> Any:
    res_regex = r"```json(.*?)```"
    res = re.findall(res_regex, input_text, re.DOTALL)
    if not res:
        match = re.search(r'\{.*\}', input_text, re.DOTALL)
        if match:
            res = match.group()
            return res
    if not res:
        return "{}"
    json_str = [r.strip() for r in res][0]
    return json_str


text = """```json{
"Military Minister": "Given our history of conflict with Country J and our reliance on guerrilla tactics and Allied support, how would you assess our current military readiness in terms of logistics, equipment modernization, and troop cohesion? Additionally, what potential strategies do you recommend for defense and potential counterattacks?",
"Finance Minister": "Considering our strained economy due to prolonged warfare and occupation, what measures can we take to stabilize our financial situation? Are there any potential sources of funding or economic relief we could explore, either through international aid or internal reforms?",
"Foreign Minister": "With the current geopolitical landscape, which countries do you believe would be the most viable partners for military alliances or non-intervention treaties, particularly in light of our past collaboration with Country U? How might our relationships with neighboring countries, such as Country H and Country P, impact our strategic options?"
}```
"""

print(extract_json(text))
