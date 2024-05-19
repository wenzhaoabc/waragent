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

**RAG**

历史事件匿名化

| Fake Name   | Real Name            | Type     |
|:------------|:---------------------|:---------|
| Country FR  | Belgium              | Country  |
| Country BE  | Germany              | Country  |
| Country GE  | Switzerland          | Country  |
| Country SW  | Italy                | Country  |
| Country IT  | Spain                | Country  |
| Country SP  | Luxembourg           | Country  |
| Country DK  | Denmark              | Country  |
| Country PO  | Poland               | Country  |
| Country AU  | Austria              | Country  |
| Country FR  | France               | Country  |
| Country CZ  | Czechoslovakia       | Country  |
| Country SW  | Switzerland          | Country  |
| Country LU  | Luxembourg           | Country  |
| Country BE  | Belgium              | Country  |
| Country NE  | Netherlands          | Country  |
| Sea NO      | North Sea            | Sea      |
| Sea BA      | Baltic Sea           | Sea      |
| Sea ME      | Mediterranean Sea    | Sea      |
| Port HA     | Hamburg              | Port     |
| Port KI     | Kiel                 | Port     |
| Ocean AT    | Atlantic Ocean       | Ocean    |
| Mountain AL | Alps                 | Mountain |
| Mountain PY | Pyrenees             | Mountain |
| Mountain MC | Massif Central       | Mountain |
| Mountain VO | Vosges               | Mountain |
| River SE    | Seine                | River    |
| River LO    | Loire                | River    |
| River GA    | Garonne              | River    |
| River RH    | Rhone                | River    |
| Mountain AL | (Alps)               | Mountain |
| Mountain HR | (Harz)               | Mountain |
| Mountain ER | (Eifel)              | Mountain |
| Mountain BO | (Bohemian Forest)    | Mountain |
| River RH    | (Rhine)              | River    |
| River EL    | (Elbe)               | River    |
| River DA    | (Danube)             | River    |
| River OD    | (Oder)               | River    |
| City BE     | (Berlin)             | City     |
| City HA     | (Hamburg)            | City     |
| City MU     | (Munich)             | City     |
| City FR     | (Frankfurt)          | City     |
| City CO     | (Cologne)            | City     |
| Area RU     | (Ruhr)               | Area     |
| City ES     | (Essen)              | City     |
| Sea EN      | (North Sea)          |          |
| Sea IR      | (Irish Sea)          |          |
| Channel EN  | (English Channel)    |          |
| Ocean AT    | (Atlantic Ocean)     |          |
| Port LO     | (London)             |          |
| Port LI     | (Liverpool)          |          |
| Port SO     | (Southampton)        |          |
| Port GL     | (Glasgow)            |          |
| Mountain GR | (Grampian Mountains) |          |
| Mountain CA | (Cambrian Mountains) |          |
| Mountain PE | (Pennines)           |          |
| River TH    | (Thames)             |          |
| River SE    | (Severn)             |          |
| River ME    | (Mersey)             |          |
| River CL    | (Clyde)              |          |
| City LO     | (London)             |          |
| City BI     | (Birmingham)         |          |
| City LI     | (Liverpool)          |          |
| City GL     | (Glasgow)            |          |
| City MA     | (Manchester)         |          |
| Ocean ME    | (Mediterranean)      |          |
| Country HU  | (Hungary)            |          |
| Country SL  | (Slovakia)           |          |
| Country RO  | (Romania)            |          |
| Country YU  | (Yugoslavia)         |          |
| Country AU  | (Austria)            |          |
| River TI    | (Tisza)              |          |
| City BU     | (Budapest)           |          |          
| City DE     | (Debrecen)           |          |          
| City SZ     | (Szeged)             |          |            
| City MI     | (Miskolc)            |          |
| City PE     | (Pécs)               |          |
| City VE     | (Veszprém)           |          |
| River DA    | (Danube)             |          |
| River TI    | (Tisza)              |          |
| City BU     | (Budapest)           |          |
| Country SU  | (Soviet Union)       |          |
| Country GE  | (Germany)            |          |
| Country PO  | (Poland)             |          |
| Country FI  | (Finland)            |          |
| Country ES  | (Estonia)            |          |
| Country LA  | (Latvia)             |          |
| Country LI  | (Lithuania)          |          |
| Country RO  | (Romania)            |          |
| Country TU  | (Turkey)             |          |
| Country IR  | (Iran)               |          |
| Country AF  | (Afghanistan)        |          |
| Country CH  | (China)              |          |
| Sea CA      | (Caspian Sea)        |          |
| Sea BL      | (Black Sea)          |          |
| Mountain UR | (Ural Mountains)     |          |
| Mountain CA | (Caucasus Mountains) |          |
| Mountain AL | (Altai Mountains)    |          |
| River VO    | (Volga River)        |          |
| River DN    | (Dnieper River)      |          |
| River OB    | (Ob River)           |          |
| River YE    | (Yenisei River)      |          |
| River LE    | (Lena River)         |          |
| City M      | (Moscow)             |          |
| City LE     | (Leningrad)          |          |
| City KI     | (Kiev)               |          |
| City NO     | (Novosibirsk)        |          |
| Region DO   | (Donbas)             |          |
| Region KU   | (Kuznetsk Basin)     |          |