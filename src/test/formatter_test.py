from collections import defaultdict
from typing import List, Dict
from pydantic import BaseModel


class NlAction(BaseModel):
    source: str
    action: str
    target: str
    message: str


def cluster_actions(actions: List[NlAction]) -> Dict[str, List[str]]:
    clusters = defaultdict(list)
    for action in actions:
        clusters[action.action].append(action.target)
    return dict(clusters)


# 使用
actions = [
    NlAction(source='s1', action='a1', target='t1', message='m1'),
    NlAction(source='s2', action='a1', target='t2', message='m2'),
    NlAction(source='s3', action='a2', target='t3', message='m3'),
]
clusters = cluster_actions(actions)
print(clusters)  # 输出: {'a1': ['t1', 't2'], 'a2': ['t3']}
