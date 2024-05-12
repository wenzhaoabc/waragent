"""
启动WebSocket
"""
import asyncio
import copy
import json

import websockets

simulate_config = {
    "history": "II",
    "trigger": "Country G betray the Non-Intervention Treaty with Country P and Country G invasion of Country P.",
    "llm": "qwen-plus",
    "round": 10,
    "knowledge": "rag",
    "tool_choice": "auto",
}
rels = {
    "rels": {
        "Country G": {
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country J": {
            "Country G": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "x",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country I": {
            "Country G": "-",
            "Country J": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country H": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country C": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country S": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country U": {
            "Country G": "-",
            "Country J": "x",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country B": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country F": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country P": "-"
        },
        "Country P": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-"
        }
    },
    "rels_pri": {
        "Country G": {
            "Country J": "-",
            "Country I": "&",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country J": {
            "Country G": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "x",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country I": {
            "Country G": "&",
            "Country J": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country H": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country C": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country S": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country U": {
            "Country G": "-",
            "Country J": "x",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country B": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country B": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country F": "-",
            "Country P": "-"
        },
        "Country F": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country P": "-"
        },
        "Country P": {
            "Country G": "-",
            "Country J": "-",
            "Country I": "-",
            "Country H": "-",
            "Country C": "-",
            "Country S": "-",
            "Country U": "-",
            "Country B": "-",
            "Country F": "-"
        }
    }
}
countries = {k: {"mobilization": False} for k, v in rels["rels"].items()}
received_requests = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Est exercitationem alias a"
questions = {
    "Military Minister": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Est exercitationem alias aspernatur eligendi nisi. Atque!",
    "Foreign Minister": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Est exercitationem alias aspernatur eligendi nisi. Atque!",
    "Finance Minister": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Est exercitationem alias aspernatur eligendi nisi. Atque!",
}
suggestions = copy.copy(questions)
actions = {"General Mobilization": "Mobilization!", "Declare War": "I will declare war to Country I",
           "Send Message": "Send message to Country I", }

mocked_data = [
    {"type": "start", "round": 1, "data": {}},
    {"type": "status", "round": 1, "data": {**rels, "countries": countries}},
    # {"type": "country", "round": 1, "data": {"country": "China", "country_name": "Country G"}},
    {"type": "process", "round": 1, "data": {"country": "Country C", "received_requests": received_requests}},
    {"type": "process", "round": 1, "data": {"country": "Country C", "questions": {**questions}}},
    {"type": "process", "round": 1, "data": {"country": "Country C", "suggestions": {**suggestions}}},
    {"type": "process", "round": 1,
     "data": {"country": "Country C", "actions": {**actions}, "thought": "I am thinking!"}},
    {"type": "status", "round": 1, "data": {**rels, "countries": countries}},
    # {"type": "end", "round": 1, "data": {**rels, "countries": countries}},
    #
    {"type": "start", "round": 2, "data": {}},
    {"type": "status", "round": 2, "data": {**rels, "countries": countries}},
    # {"type": "country", "round": 1, "data": {"country": "China", "country_name": "Country G"}},
    {"type": "process", "round": 2, "data": {"country": "Country U", "received_requests": received_requests}},
    {"type": "process", "round": 2, "data": {"country": "Country U", "questions": {**questions}}},
    {"type": "process", "round": 2, "data": {"country": "Country U", "suggestions": {**suggestions}}},
    {"type": "process", "round": 2,
     "data": {"country": "Country U", "actions": {**actions}, "thought": "I am thinking!"}},
    {"type": "status", "round": 2, "data": {**rels, "countries": countries}},
    {"type": "end", "round": 2, "data": {**rels, "countries": countries}},
]

# async def echo(websocket, path):
#     global simulate_config
#     async for message in websocket:
#         message = json.loads(message)
#         if message["type"] != "start":
#             continue
#         config = message["data"]
#         simulate_config = {**simulate_config, **config}
#         print(simulate_config)
#         for data in mocked_data:
#             await asyncio.sleep(1)
#             await websocket.send(json.dumps(data))
#
#
# start_server = websockets.serve(echo, "localhost", 8765)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

# start_server = websockets.serve(echo, "localhost", 8765)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

import os

for data in mocked_data:
    with open(f"{os.getenv('ROOT_PATH')}/static/demo1.txt", 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=True) + "\n")
