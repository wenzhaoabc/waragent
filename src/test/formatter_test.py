from collections import defaultdict
from typing import List, Dict
from src.prompts.struct_format import Formatter, NlAction

formatter = Formatter(None)


def testFormat():
    # 使用
    actions = [
        NlAction(source="s1", action="a1", target="t1", message="m1"),
        NlAction(source="s1", action="a1", target="t2", message="m2"),
        NlAction(source="s1", action="a2", target="t3", message="m3"),
    ]
    clusters = formatter.nlaction_str(actions)
    print(clusters)  # 输出: {'a1': ['t1', 't2'], 'a2': ['t3']}
    print(len(clusters))  # 输出: 2
