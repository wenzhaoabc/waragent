# War Agent

基于LLM与KG的历史战争模拟器

## 项目架构

ActionTypyList

Empty Input:        Wait Without Action, General Mobilization, 
Dict Input:         Present Peace Agreement, Send Message
Country List Input: ...15 actions

Board & Stick

Board : Public global situation
Stick : Single country situation

## 数据存储

**Neo4J**
```shell
sudo docker run -d \
    --user "$(id -u):$(id -g)" \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_PLUGINS='["apoc","apoc-extended","graph-data-science"]' \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/plugins:/plugins \
    neo4j:latest
```


