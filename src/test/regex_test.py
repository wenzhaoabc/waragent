import re
import json

text = """
Thought Process:
1. Identify Potential Ally Countries:
   - Direct allies: United States, Canada, Australia, New Zealand
   - Enemies of Country G (Germany): Soviet Union, China, United States, possibly others
   - Allies of United States: Could be UK, Canada, Australia, New Zealand, Soviet Union
   - Allies of Soviet Union: Could be China, possibly UK due to shared enemy in Country G

2. Analyze Potential Ally Actions:
   - Allies are likely to be concerned about the aggressive actions of Country G and Country J. We should coordinate with them to ensure unity in response.

3. Identify Potential Enemy Countries:
   - Direct enemies: Country G (Germany), Country J (Japan)
   - Enemies of UK allies: Country G, Country J
   - Allies of Country G: Italy (at least initially)
   - Allies of Country J: None mentioned, but could potentially form alliances with countries opposing the Allies

4. Analyze Potential Enemy Actions:
   - Country G and Country J are expansionist and may attempt to disrupt Allied cohesion through propaganda, subversion, or military action.

5. First Actions to Perform:
   - Request Military Alliance with United States, Canada, Australia, and New Zealand to solidify our alliance and deter aggression.
   - Send Message to Soviet Union to explore potential collaboration against common enemies.
   - Request Non-Intervention Treaty with Italy to prevent them from assisting our enemies.

6. Summarize Analysis on Situation:
   - The UK should focus on strengthening its existing alliances and preventing new ones from forming against us. We should also communicate with potential neutral or unaligned countries to prevent them from joining our enemies.

Actions to Perform:
```json
{
  "Request Military Alliance": ["United States", "Canada", "Australia", "New Zealand"],
  "Send Message": {
    "Soviet Union": {"content": "The United Kingdom proposes a cooperative effort against mutual threats in the current global climate."},
    "Italy": {"content": "We are interested in establishing a non-intervention treaty to ensure neither of our nations becomes embroiled in each other's conflicts."}
  }
}
```
"""


def test_extract_json():
    thought_process = text.replace(r"(?s)```json.*?```", "")
    print("thought_process")
    print(thought_process)
    res_regex = r"```json(.*?)```"
    res = re.findall(res_regex, text, re.DOTALL)
    print("res")
    print(res)
    actions_str = [item.strip() for item in res][0]
    print("actions_str")
    print(actions_str)
    actions = json.loads(actions_str)
    print(actions)
    pass


if __name__ == "__main__":
    test_extract_json()
