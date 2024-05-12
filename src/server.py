import asyncio
import json
import multiprocessing
import os
import time

import websockets
import requests

from src.datasource.neo4jdata.neo4j_db import Neo4JDB
from src.t2kg import extract_kgs_neo4j


def text_kg_process(pipe, text):
    """文本到知识图谱进程"""

    def callback(msg):
        print(msg)
        msg["status"] = 2
        pipe.send(json.dumps(msg))

    headers = {
        "Authorization": f"Bearer {os.getenv('')}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": "Alice lawyer is 25 years old and Bob is her roommate since 2001. Bob works as a journalist. Alice owns a the webpage www.alice.com and Bob owns the webpage www.bob.com.",
        "datasetId": "6634e35edc5e75c5ce163d10",
        "name": "测试训练",
        "trainingType": "chunk",
        "chunkSize": 2000,
    }
    post_url = "https://fastgpt.wenzhaoabc.com/api/core/dataset/collection/create/text"
    response = requests.post(post_url, headers=headers, json=payload)
    pipe.send(json.dumps({"status": 3}))
    neo4j_db = Neo4JDB()
    kgs_neo4j = extract_kgs_neo4j(text, neo4j_db, callback)


async def handle_file_upload(websocket, path):
    """处理文件上传的逻辑"""
    file_content = await websocket.recv()
    print(file_content)
    await websocket.send(json.dumps({"status": 1}))
    parent_pipe, child_pipe = multiprocessing.Pipe()  # 创建管道
    p = multiprocessing.Process(target=text_kg_process, args=(child_pipe, file_content))
    p.start()

    while True:
        if parent_pipe.poll():  # 检查管道是否有新的数据
            message = parent_pipe.recv()  # 从管道读取数据
            await websocket.send(message)  # 将数据发送给前端

            if json.loads(message).get("type") == "execute_result":
                await websocket.send(json.dumps({"status": 0}))
                break
        await asyncio.sleep(0.5)  # 暂停一段时间，以减少CPU使用率


async def handle_simulate(websocket, path):
    param = await websocket.recv()  # 从客户端接收参数
    print(f"从客户端接收到的参数: {param}")
    parent_pipe, child_pipe = multiprocessing.Pipe()  # 创建管道
    p = multiprocessing.Process(target=simulate_process, args=(child_pipe, param))  # 使用接收到的参数创建新进程
    p.start()  # 启动新进程

    while True:
        if parent_pipe.poll():  # 检查管道是否有新的数据
            message = parent_pipe.recv()  # 从管道读取数据
            print(message)
            await websocket.send(message)  # 将数据发送给前端
        await asyncio.sleep(1)  # 暂停一段时间，以减少CPU使用率


def simulate_process(pipe, param):
    param = json.loads(param)
    if param["type"] == "start":
        default = {
            "history": "II",
            "llm": "qwen-plus",
            "round": 10,
            "tool_choice": "auto",
            "knowledge": "rag",
            "trigger": "Country J betray the Non-Intervention Treaty with Country P and Country J invasion of Country P."
        }
        config = {**default, **param["data"]}
        from src.main import start_simulate
        start_simulate(pipe=pipe, config=config)
    elif param["type"] == "demo":
        with open(f"{os.getenv('ROOT_PATH')}/static/demo1.txt", "r", encoding="utf-8") as f:
            for line in f:
                pipe.send(line)
                time.sleep(1)


async def websocket_server(websocket, path):
    print(path)
    while True:
        if path == "/simulate":
            await handle_simulate(websocket, path)
        elif path == "/upload":
            await handle_file_upload(websocket, path)


if __name__ == "__main__":
    start_server = websockets.serve(websocket_server, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
