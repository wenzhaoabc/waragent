"""
Process log files.
"""
import os
import datetime
from .log import logger

filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def output(content: any) -> None:
    print(content, end="")
    logger.info(content)
    log_file = os.getenv("ROOT_PATH") + f"/{filename}-log.txt"
    with open(f"{log_file}", mode='a', encoding='utf-8') as f:
        f.write(content)
