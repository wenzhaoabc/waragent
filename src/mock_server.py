"""
启动WebSocket
"""

import asyncio
import copy
import json
import multiprocessing
import os

from src.main import start_simulate


async def _start_simulate():
    parent_pipe, child_pipe = multiprocessing.Pipe()  # 创建管道
    model = os.getenv("LLM_MODEL")
    pipe_file = os.getenv("PIPE_FILE")
    p = multiprocessing.Process(
        target=start_simulate, kwargs={"pipe": child_pipe, "llm": model}
    )  # 使用接收到的参数创建新进程
    p.start()  # 启动新进程

    try:
        while True:
            if parent_pipe.poll():  # 检查管道是否有新的数据
                message = parent_pipe.recv()  # 从管道读取数据
                if message == "END":
                    parent_pipe.send("TERMINATE")  # 发送终止信号给子进程
                    break
                with open(
                    f'{os.getenv("ROOT_PATH")}/static/simulate_logs/minister_tool_{model}_2.txt',
                    "a",
                ) as f:
                    f.write(json.dumps(message) + "\n")
            await asyncio.sleep(0.5)  # 等待0.5秒
    finally:
        parent_pipe.close()
        p.join()  # 等待子进程结束


if __name__ == "__main__":
    try:
        asyncio.run(_start_simulate())
    except KeyboardInterrupt:
        print("Process interrupted by user")
