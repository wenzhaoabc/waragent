"""
Process log files.
"""
import json
import os
from typing import Literal

from .log import logger
from .log import filename

def output(content: any) -> None:
    print(content, end="")
    logger.info("console output : \n"+content)
    log_file = os.getenv("ROOT_PATH") + f"/logs/{filename}-log-console.txt"
    with open(f"{log_file}", mode='a', encoding='utf-8') as f:
        f.write(content)


def initialize_pipe(pipe):
    def fun(type: Literal["start", "status", "process", "end"], round: int, content: any) -> None:
        data = json.dumps({"type": type, "round": round, "data": {**content}})
        pipe.send(data)
        with open(os.getenv("ROOT_PATH") + f"/logs/{filename}-json-web.txt", mode='a', encoding='utf-8') as f:
            f.write(data + "\n")

    return fun


def dump_json(type: Literal["start", "status", "process", "end"], round: int, content: any) -> None:
    data = json.dumps({"type": type, "round": round, "data": {**content}})
    with open(os.getenv("ROOT_PATH") + f"/logs/{filename}-log.json", mode='a', encoding='utf-8') as f:
        f.write(data + "\n")
