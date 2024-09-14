# War Agent

Historical War Simulation Based on LLM and KG.

## Project Structure

One main decision-making agent and four auxiliary agents.

Board : Public global situation
Stick : Single country situation

1. only president : branch [rq1_only_president](https://github.com/wenzhaoabc/waragent/tree/rq1_only_president)
2. president with minister : branch [rq2_president_minister](https://github.com/wenzhaoabc/waragent/tree/rq2_president_minister)
3. president with minister and external tools : branch [rq3_president_minister_tool](https://github.com/wenzhaoabc/waragent/tree/rq3_president_minister_tool)

## Data Storage

1. vector database
2. graph database

## Research Questions

1. The quality of the simulation system
2. The reason of the war


## Quick Start

```bash
git clone https://github.com/wenzhaoabc/waragent.git
git checkout rq3_president_minister_tool

cd waragent
pip install -r requirements.txt
python src/main.py
```