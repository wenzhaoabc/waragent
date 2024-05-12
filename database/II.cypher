// 创建Year节点
CREATE (:Year {year: 1913})
CREATE (:Year {year: 1930})
CREATE (:Year {year: 1933})
CREATE (:Year {year: 1934})
CREATE (:Year {year: 1935})
CREATE (:Year {year: 1936})
CREATE (:Year {year: 1937})
CREATE (:Year {year: 1938})

// 创建Country节点
MERGE (usa:Country {name: "United States"})
MERGE (uk:Country {name: "Britain"})
MERGE (germany:Country {name: "Germany"})
MERGE (france:Country {name: "France"})
MERGE (italy:Country {name: "Italy"})
MERGE (russia:Country {name: "Soviet_Union"})
MERGE (japan:Country {name: "Japan"})
MERGE (china:Country {name: "China"})
MERGE (poland:Country {name: "Poland"})
MERGE (hungary:Country {name:"Hungary"})

// 工业化水平
CREATE (:Metric {type: "IndustrializationLevel", value: 126})-[:HAS_METRIC {inYear: 1913}]->(usa)
CREATE (:Metric {type: "IndustrializationLevel", value: 115})-[:HAS_METRIC {inYear: 1913}]->(uk)
CREATE (:Metric {type: "IndustrializationLevel", value: 85})-[:HAS_METRIC {inYear: 1913}]->(germany)
CREATE (:Metric {type: "IndustrializationLevel", value: 59})-[:HAS_METRIC {inYear: 1913}]->(france)
CREATE (:Metric {type: "IndustrializationLevel", value: 26})-[:HAS_METRIC {inYear: 1913}]->(italy)
CREATE (:Metric {type: "IndustrializationLevel", value: 20})-[:HAS_METRIC {inYear: 1913}]->(russia)
CREATE (:Metric {type: "IndustrializationLevel", value: 20})-[:HAS_METRIC {inYear: 1913}]->(japan)

// 钢铁产量
CREATE (:Metric {type: "SteelProduction", value: 31.8})-[:HAS_METRIC {inYear: 1913}]->(usa)
CREATE (:Metric {type: "SteelProduction", value: 17.6})-[:HAS_METRIC {inYear: 1913}]->(germany)
CREATE (:Metric {type: "SteelProduction", value: 7.7})-[:HAS_METRIC {inYear: 1913}]->(uk)
CREATE (:Metric {type: "SteelProduction", value: 4.8})-[:HAS_METRIC {inYear: 1913}]->(russia)
CREATE (:Metric {type: "SteelProduction", value: 4.6})-[:HAS_METRIC {inYear: 1913}]->(france)
CREATE (:Metric {type: "SteelProduction", value: 0.93})-[:HAS_METRIC {inYear: 1913}]->(italy)
CREATE (:Metric {type: "SteelProduction", value: 0.25})-[:HAS_METRIC {inYear: 1913}]->(japan)

// 能源消耗
CREATE (:Metric {type: "EnergyConsumption", value: 541})-[:HAS_METRIC {inYear: 1913}]->(usa)
CREATE (:Metric {type: "EnergyConsumption", value: 195})-[:HAS_METRIC {inYear: 1913}]->(uk)
CREATE (:Metric {type: "EnergyConsumption", value: 187})-[:HAS_METRIC {inYear: 1913}]->(germany)
CREATE (:Metric {type: "EnergyConsumption", value: 62.5})-[:HAS_METRIC {inYear: 1913}]->(france)
CREATE (:Metric {type: "EnergyConsumption", value: 54})-[:HAS_METRIC {inYear: 1913}]->(russia)
CREATE (:Metric {type: "EnergyConsumption", value: 23})-[:HAS_METRIC {inYear: 1913}]->(japan)
CREATE (:Metric {type: "EnergyConsumption", value: 11})-[:HAS_METRIC {inYear: 1913}]->(italy)

// 制造业份额
CREATE (:Metric {type: "ManufacturingShare", value: 32.0})-[:HAS_METRIC {inYear: 1913}]->(usa)
CREATE (:Metric {type: "ManufacturingShare", value: 14.8})-[:HAS_METRIC {inYear: 1913}]->(germany)
CREATE (:Metric {type: "ManufacturingShare", value: 13.6})-[:HAS_METRIC {inYear: 1913}]->(uk)
CREATE (:Metric {type: "ManufacturingShare", value: 8.2})-[:HAS_METRIC {inYear: 1913}]->(russia)
CREATE (:Metric {type: "ManufacturingShare", value: 6.1})-[:HAS_METRIC {inYear: 1913}]->(france)
CREATE (:Metric {type: "ManufacturingShare", value: 2.4})-[:HAS_METRIC {inYear: 1913}]->(italy)
CREATE (:Metric {type: "ManufacturingShare", value: 1.0})-[:HAS_METRIC {inYear: 1913}]->(japan)

// 工业潜力
CREATE (:Metric {type: "IndustrialPotential", value: 289.1})-[:HAS_METRIC {inYear: 1913}]->(usa)
CREATE (:Metric {type: "IndustrialPotential", value: 137.7})-[:HAS_METRIC {inYear: 1913}]->(germany)
CREATE (:Metric {type: "IndustrialPotential", value: 127.2})-[:HAS_METRIC {inYear: 1913}]->(uk)
CREATE (:Metric {type: "IndustrialPotential", value: 76.6})-[:HAS_METRIC {inYear: 1913}]->(russia)
CREATE (:Metric {type: "IndustrialPotential", value: 57.3})-[:HAS_METRIC {inYear: 1913}]->(france)
CREATE (:Metric {type: "IndustrialPotential", value: 25.1})-[:HAS_METRIC {inYear: 1913}]->(japan)
CREATE (:Metric {type: "IndustrialPotential", value: 22.5})-[:HAS_METRIC {inYear: 1913}]->(italy)


// 国防开支度量值 - 1930年
CREATE (:Metric {type: "DefenseExpenditure", value: 218})-[:HAS_METRIC {inYear: 1930}]->(japan)
CREATE (:Metric {type: "DefenseExpenditure", value: 266})-[:HAS_METRIC {inYear: 1930}]->(italy)
CREATE (:Metric {type: "DefenseExpenditure", value: 162})-[:HAS_METRIC {inYear: 1930}]->(germany)
CREATE (:Metric {type: "DefenseExpenditure", value: 722})-[:HAS_METRIC {inYear: 1930}]->(russia)
CREATE (:Metric {type: "DefenseExpenditure", value: 512})-[:HAS_METRIC {inYear: 1930}]->(uk)
CREATE (:Metric {type: "DefenseExpenditure", value: 498})-[:HAS_METRIC {inYear: 1930}]->(france)
CREATE (:Metric {type: "DefenseExpenditure", value: 699})-[:HAS_METRIC {inYear: 1930}]->(usa)

// 国防开支度量值 - 1933年
CREATE (:Metric {type: "DefenseExpenditure", value: 183})-[:HAS_METRIC {inYear: 1933}]->(japan)
CREATE (:Metric {type: "DefenseExpenditure", value: 351})-[:HAS_METRIC {inYear: 1933}]->(italy)
CREATE (:Metric {type: "DefenseExpenditure", value: 361})-[:HAS_METRIC {inYear: 1933}]->(germany)
CREATE (:Metric {type: "DefenseExpenditure", value: 303})-[:HAS_METRIC {inYear: 1933}]->(russia)
CREATE (:Metric {type: "DefenseExpenditure", value: 533})-[:HAS_METRIC {inYear: 1933}]->(uk)
CREATE (:Metric {type: "DefenseExpenditure", value: 500})-[:HAS_METRIC {inYear: 1933}]->(france)
CREATE (:Metric {type: "DefenseExpenditure", value: 792})-[:HAS_METRIC {inYear: 1933}]->(usa)

// 国防开支度量值 - 1934年
CREATE (:Metric {type: "DefenseExpenditure", value: 292})-[:HAS_METRIC {inYear: 1934}]->(japan)
CREATE (:Metric {type: "DefenseExpenditure", value: 455})-[:HAS_METRIC {inYear: 1934}]->(italy)
CREATE (:Metric {type: "DefenseExpenditure", value: 709})-[:HAS_METRIC {inYear: 1934}]->(germany)
CREATE (:Metric {type: "DefenseExpenditure", value: 3479})-[:HAS_METRIC {inYear: 1934}]->(russia)
CREATE (:Metric {type: "DefenseExpenditure", value: 540})-[:HAS_METRIC {inYear: 1934}]->(uk)
CREATE (:Metric {type: "DefenseExpenditure", value: 707})-[:HAS_METRIC {inYear: 1934}]->(france)
CREATE (:Metric {type: "DefenseExpenditure", value: 803})-[:HAS_METRIC {inYear: 1934}]->(usa)

// 国防开支度量值 - 1935年
CREATE (:Metric {type: "DefenseExpenditure", value: 313})-[:HAS_METRIC {inYear: 1935}]->(japan)
CREATE (:Metric {type: "DefenseExpenditure", value: 1149})-[:HAS_METRIC {inYear: 1935}]->(italy)
CREATE (:Metric {type: "DefenseExpenditure", value: 2332})-[:HAS_METRIC {inYear: 1935}]->(germany)
CREATE (:Metric {type: "DefenseExpenditure", value: 2933})-[:HAS_METRIC {inYear: 1935}]->(russia)
CREATE (:Metric {type: "DefenseExpenditure", value: 892})-[:HAS_METRIC {inYear: 1935}]->(uk)
CREATE (:Metric {type: "DefenseExpenditure", value: 980})-[:HAS_METRIC {inYear: 1935}]->(france)
CREATE (:Metric {type: "DefenseExpenditure", value: 932})-[:HAS_METRIC {inYear: 1935}]->(usa)

// 国防开支度量值 - 1936年
CREATE (:Metric {type: "DefenseExpenditure", value: 940})-[:HAS_METRIC {inYear: 1936}]->(japan)
CREATE (:Metric {type: "DefenseExpenditure", value: 1015})-[:HAS_METRIC {inYear: 1936}]->(italy)
CREATE (:Metric {type: "DefenseExpenditure", value: 4793})-[:HAS_METRIC {inYear: 1936}]->(germany)
CREATE (:Metric {type: "DefenseExpenditure", value: 3430})-[:HAS_METRIC {inYear: 1936}]->(russia)
CREATE (:Metric {type: "DefenseExpenditure", value: 1283})-[:HAS_METRIC {inYear: 1936}]->(uk)
CREATE (:Metric {type: "DefenseExpenditure", value: 862})-[:HAS_METRIC {inYear: 1936}]->(france)
CREATE (:Metric {type: "DefenseExpenditure", value: 1032})-[:HAS_METRIC {inYear: 1936}]->(usa)

// 国防开支度量值 - 1937年
CREATE (:Metric {type: "DefenseExpenditure", value: 1740})-[:HAS_METRIC {inYear: 1937}]->(japan)
CREATE (:Metric {type: "DefenseExpenditure", value: 746})-[:HAS_METRIC {inYear: 1937}]->(italy)
CREATE (:Metric {type: "DefenseExpenditure", value: 7415})-[:HAS_METRIC {inYear: 1937}]->(germany)
CREATE (:Metric {type: "DefenseExpenditure", value: 5429})-[:HAS_METRIC {inYear: 1937}]->(russia)
CREATE (:Metric {type: "DefenseExpenditure", value: 1863})-[:HAS_METRIC {inYear: 1937}]->(uk)
CREATE (:Metric {type: "DefenseExpenditure", value: 919})-[:HAS_METRIC {inYear: 1937}]->(france)
CREATE (:Metric {type: "DefenseExpenditure", value: 1131})-[:HAS_METRIC {inYear: 1937}]->(usa)

// 国防开支度量值 - 1938年
CREATE (:Metric {type: "DefenseExpenditure", value: 2489})-[:HAS_METRIC {inYear: 1938}]->(japan)
CREATE (:Metric {type: "DefenseExpenditure", value: 818})-[:HAS_METRIC {inYear: 1938}]->(italy)
CREATE (:Metric {type: "DefenseExpenditure", value: 5807})-[:HAS_METRIC {inYear: 1938}]->(germany)
CREATE (:Metric {type: "DefenseExpenditure", value: 4527})-[:HAS_METRIC {inYear: 1938}]->(russia)
CREATE (:Metric {type: "DefenseExpenditure", value: 1915})-[:HAS_METRIC {inYear: 1938}]->(uk)
CREATE (:Metric {type: "DefenseExpenditure", value: 1014})-[:HAS_METRIC {inYear: 1938}]->(france)
CREATE (:Metric {type: "DefenseExpenditure", value: 1706})-[:HAS_METRIC {inYear: 1938}]->(usa)


=================
MERGE (usa:Country {name: "United States"})
MERGE (uk:Country {name: "Britain"})
MERGE (germany:Country {name: "Germany"})
MERGE (france:Country {name: "France"})
MERGE (italy:Country {name: "Italy"})
MERGE (russia:Country {name: "Soviet_Union"})
MERGE (japan:Country {name: "Japan"})
MERGE (china:Country {name: "China"})
MERGE (poland:Country {name: "Poland"})
MERGE (hungary:Country {name:"Hungary"})

MERGE (gdp:Finance {name:"gdp"})
MERGE (army:Military {name:"army"})
MERGE (tank:Military {name:"tank"})


CREATE (usa)-[:HAS {inYear: 1940, value:2000}]->(gdp)
CREATE (russia)-[:HAS {inYear: 1941, value:433}]->(gdp)
CREATE (usa)-[:HAS {inYear: 1940, value:100000, type:"number of people"}]->(army)
CREATE (usa)-[:HAS {inYear: 1940, value:300, type:"number"}]->(tank)