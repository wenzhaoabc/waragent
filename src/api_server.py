"""
This is a simple FastAPI server that support the world war II simulation.
"""

import os
import json
import shutil
import asyncio
import aiofiles
import aiohttp
from datetime import datetime
from fastapi import FastAPI, UploadFile, WebSocket, File
from fastapi.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pipe

from src.main import start_simulate
from src.datasource.neo4jdata.neo4j_db import Neo4JDB
from src.t2kg import extract_kgs_neo4j
from src.agents.tools import KnowledgeRetrieval

app = FastAPI(debug=True, title="WarAgent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/upload")
async def options_upload_file():
    return {}


@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    filename = datetime.now().strftime("%Y%m%d-%H%M%S") + str(file.filename).replace(
        " ", "_"
    )
    with open(f"static/{filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": filename}


@app.websocket("/import")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    request_params = await websocket.receive_json()
    filename = request_params["filename"]
    async with aiofiles.open(f"static/{filename}", "r", encoding="utf-8") as f:
        text = await f.read()

    post_url = "https://fastgpt.wenzhaoabc.com/api/core/dataset/collection/create/text"
    headers = {
        "Authorization": f"Bearer {os.getenv('RAG_KB_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "datasetId": "6649852eff0a4fb917024cbe",
        "name": filename.split(".")[0],
        "trainingType": "chunk",
        "chunkSize": 2000,
    }
    post_url = "https://fastgpt.wenzhaoabc.com/api/core/dataset/collection/create/text"
    async with aiohttp.ClientSession() as session:
        async with session.post(post_url, headers=headers, json=payload) as response:
            response = await response.json()
            await websocket.send_text(json.dumps({"type": "rag", "data": response}))

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        kwargs = {
            "text": text,
            "neo4j": Neo4JDB(),
            "callback": lambda x: asyncio.run_coroutine_threadsafe(
                websocket.send_text(json.dumps(x)), loop
            ),
            "model": "qwen-max",
        }
        func = partial(extract_kgs_neo4j, **kwargs)
        feature = loop.run_in_executor(executor, func)
        while True:
            if feature.done():
                await websocket.send_text(json.dumps({"type": "end"}))
                break
            else:
                await asyncio.sleep(1)
    await websocket.close()


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    r = KnowledgeRetrieval()
    while True:
        data = await websocket.receive_json()
        if data["type"] == "end":
            break
        question = data["question"]
        llm = data.get("llm", "qwen-max")
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            kg_future = loop.run_in_executor(executor, r.run, question, "kg")
            rag_future = loop.run_in_executor(executor, r.run, question, "rag")
            kg_res = await kg_future
            await websocket.send_json({"type": "kg", "data": kg_res})
            rag_res = await rag_future
            await websocket.send_json({"type": "rag", "data": rag_res})
    await websocket.close()


# websocket server
@app.websocket("/simulate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    request_params = await websocket.receive_json()
    print(request_params)
    if request_params["type"] == "config":
        # start simulation
        if request_params["data"]["type"] == "new":
            # start a new process and receice the data from the pipe
            parent_conn, child_conn = Pipe()
            with ThreadPoolExecutor() as executor:
                kwargs = {
                    "pipe": child_conn,
                    "config": request_params["data"]["config"],
                }  # replace with your arguments
                func = partial(start_simulate, **kwargs)
                loop = asyncio.get_event_loop()
                feature = loop.run_in_executor(executor, func)
                while True:
                    if parent_conn.poll():
                        data = parent_conn.recv()
                        await websocket.send_text(data)
                    elif feature.done():
                        await websocket.send_text(json.dumps({"type": "end"}))
                        break
                    else:
                        await asyncio.sleep(1)
        elif request_params["data"]["type"] == "demo":
            # read the demo data from the file and send it to the client
            demo_file = request_params["data"]["file"]
            async with aiofiles.open(
                f"{os.getenv('ROOT_PATH')}/static/simulate_logs/{demo_file}.txt",
                "r",
                encoding="utf-8",
            ) as f:
                async for line in f:
                    # when client close the connection, the loop will break
                    if websocket.client_state == WebSocketState.DISCONNECTED:
                        break
                    await websocket.send_text(line.strip())
                    await asyncio.sleep(1)
                # await websocket.send_text(f'"{json.dumps({"type": "end"})}"')
            await websocket.close()

    elif request_params["type"] == "stop":
        pass

    await websocket.close()


@app.get("/")
async def app_dev_test(q: str = None):
    from src.datasource.neo4jdata.neo4j_db import Neo4JDB
    from src.datasource import Neo4jAnswers
    from src.llm import LLM

    neo4j = Neo4JDB()
    schema = neo4j.get_schema()
    print(schema)
    na = Neo4jAnswers(LLM('gpt-4o'))
    question = q
    answer = na.neo4j_answers(question)
    print(answer)
    return {"schema": schema, "answer": answer}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_server:app", host="127.0.0.1", port=8765, reload=True)
