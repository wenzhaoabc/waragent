## Part 1 国家基本属性信息

// 创建国家节点并添加属性
MERGE (usa:Country {name: "United States", climate: "varied", area: "9,833,520 km²", location: "North America"})
MERGE (uk:Country {name: "Britain", climate: "temperate", area: "243,610 km²", location: "Europe"})
MERGE (germany:Country {name: "Germany", climate: "temperate", area: "357,022 km²", location: "Europe"})
MERGE (france:Country {name: "France", climate: "temperate", area: "643,801 km²", location: "Europe"})
MERGE (italy:Country {name: "Italy", climate: "Mediterranean", area: "301,340 km²", location: "Europe"})
MERGE (russia:Country {name: "Soviet Union", climate: "varied", area: "22,402,200 km²", location: "Eurasia"})
MERGE (japan:Country {name: "Japan", climate: "varied", area: "377,975 km²", location: "Asia"})
MERGE (china:Country {name: "China", climate: "varied", area: "9,596,961 km²", location: "Asia"})
MERGE (poland:Country {name: "Poland", climate: "temperate", area: "312,696 km²", location: "Europe"})
MERGE (hungary:Country {name:"Hungary", climate: "continental", area: "93,030 km²", location: "Europe"})

// 添加相对位置关系
MERGE (usa)-[:NEIGHBORS {description: "across the Atlantic Ocean from"}]->(uk)
MERGE (uk)-[:NEIGHBORS {description: "across the English Channel from"}]->(france)
MERGE (france)-[:NEIGHBORS {description: "borders"}]->(germany)
MERGE (germany)-[:NEIGHBORS {description: "borders"}]->(poland)
MERGE (poland)-[:NEIGHBORS {description: "borders"}]->(soviet_union)
MERGE (italy)-[:NEIGHBORS {description: "borders"}]->(france)
MERGE (italy)-[:NEIGHBORS {description: "borders"}]->(germany)
MERGE (hungary)-[:NEIGHBORS {description: "borders"}]->(germany)
MERGE (hungary)-[:NEIGHBORS {description: "borders"}]->(soviet_union)
MERGE (japan)-[:NEIGHBORS {description: "across the Sea of Japan from"}]->(soviet_union)
MERGE (japan)-[:NEIGHBORS {description: "across the East China Sea from"}]->(china)
MERGE (china)-[:NEIGHBORS {description: "borders"}]->(soviet_union)




## Part 2 国家人口信息 - 1939年
MERGE (germany)-[:HAS_POPULATION]->(pop_germany:Population {total: 69.6, male: 48.5, female: 51.5})
MERGE (japan)-[:HAS_POPULATION]->(pop_japan:Population {total: 71.4, male: 49.0, female: 51.0})
MERGE (italy)-[:HAS_POPULATION]->(pop_italy:Population {total: 43.8, male: 48.7, female: 51.3})
MERGE (hungary)-[:HAS_POPULATION]->(pop_hungary:Population {total: 9.1, male: 48.8, female: 51.2})
MERGE (china)-[:HAS_POPULATION]->(pop_china:Population {total: 540.0, male: 50.1, female: 49.9})
MERGE (russia)-[:HAS_POPULATION]->(pop_russia:Population {total: 168.5, male: 48.7, female: 51.3})
MERGE (usa)-[:HAS_POPULATION]->(pop_usa:Population {total: 131.0, male: 49.0, female: 51.0})
MERGE (uk)-[:HAS_POPULATION]->(pop_uk:Population {total: 47.6, male: 48.6, female: 51.4})
MERGE (france)-[:HAS_POPULATION]->(pop_france:Population {total: 41.7, male: 48.4, female: 51.6})
MERGE (poland)-[:HAS_POPULATION]->(pop_poland:Population {total: 34.8, male: 48.5, female: 51.5})


## Part 3 钢铁年产量
// 美国钢铁产量
MERGE (usa:Country {name: "United States"})
MERGE (usa1913:Steel {inYear: 1913, production: 3180})
MERGE (usa)-[:PRODUCED]->(usa1913)
MERGE (usa1940:Steel {inYear: 1940, production: 6076})
MERGE (usa)-[:PRODUCED]->(usa1940)
MERGE (usa1941:Steel {inYear: 1941, production: 7510})
MERGE (usa)-[:PRODUCED]->(usa1941)
MERGE (usa1943:Steel {inYear: 1943, production: 8059})
MERGE (usa)-[:PRODUCED]->(usa1943)
MERGE (usa1944:Steel {inYear: 1944, production: 8132})
MERGE (usa)-[:PRODUCED]->(usa1944)

// 德国钢铁产量
MERGE (germany:Country {name: "Germany"})
MERGE (germany1913:Steel {inYear: 1913, production: 1832})
MERGE (germany)-[:PRODUCED]->(germany1913)
MERGE (germany1940:Steel {inYear: 1940, production: 2154})
MERGE (germany)-[:PRODUCED]->(germany1940)
MERGE (germany1942:Steel {inYear: 1942, production: 2048})
MERGE (germany)-[:PRODUCED]->(germany1942)

// 德国钢铁产量(含占领区)
MERGE (germany1940o:Steel {inYear: 1940, production: 2610})
MERGE (germany)-[:PRODUCED]->(germany1940o)
MERGE (germany1941o:Steel {inYear: 1941, production: 3180})
MERGE (germany)-[:PRODUCED]->(germany1941o)
MERGE (germany1942o:Steel {inYear: 1942, production: 3210})
MERGE (germany)-[:PRODUCED]->(germany1942o)
MERGE (germany1943o:Steel {inYear: 1943, production: 3460})
MERGE (germany)-[:PRODUCED]->(germany1943o)
MERGE (germany1944o:Steel {inYear: 1944, production: 2850})
MERGE (germany)-[:PRODUCED]->(germany1944o)

// 苏联钢铁产量
MERGE (russia:Country {name: "Soviet Union"})
MERGE (russia1913:Steel {inYear: 1913, production: 423})
MERGE (russia)-[:PRODUCED]->(russia1913)
MERGE (russia1940:Steel {inYear: 1940, production: 1832})
MERGE (russia)-[:PRODUCED]->(russia1940)
MERGE (russia1942:Steel {inYear: 1942, production: 810})
MERGE (russia)-[:PRODUCED]->(russia1942)
MERGE (russia1943:Steel {inYear: 1943, production: 850})
MERGE (russia)-[:PRODUCED]->(russia1943)
MERGE (russia1944:Steel {inYear: 1944, production: 1000})
MERGE (russia)-[:PRODUCED]->(russia1944)
MERGE (russia1945:Steel {inYear: 1945, production: 1230})
MERGE (russia)-[:PRODUCED]->(russia1945)

// 英国钢铁产量
MERGE (uk:Country {name: "Britain"})
MERGE (uk1913:Steel {inYear: 1913, production: 778})
MERGE (uk)-[:PRODUCED]->(uk1913)
MERGE (uk1939:Steel {inYear: 1939, production: 1343})
MERGE (uk)-[:PRODUCED]->(uk1939)
MERGE (uk1940:Steel {inYear: 1940, production: 1230})
MERGE (uk)-[:PRODUCED]->(uk1940)
MERGE (uk1943:Steel {inYear: 1943, production: 1300})
MERGE (uk)-[:PRODUCED]->(uk1943)

// 法国钢铁产量
MERGE (france:Country {name: "France"})
MERGE (france1913:Steel {inYear: 1913, production: 469})
MERGE (france)-[:PRODUCED]->(france1913)
MERGE (france1939:Steel {inYear: 1939, production: 811})
MERGE (france)-[:PRODUCED]->(france1939)

// 意大利钢铁产量
MERGE (italy:Country {name: "Italy"})
MERGE (italy1913:Steel {inYear: 1913, production: 93})
MERGE (italy)-[:PRODUCED]->(italy1913)
MERGE (italy1940:Steel {inYear: 1940, production: 226})
MERGE (italy)-[:PRODUCED]->(italy1940)

// 日本钢铁产量
MERGE (japan:Country {name: "Japan"})
MERGE (japan1913:Steel {inYear: 1913, production: 26})
MERGE (japan)-[:PRODUCED]->(japan1913)
MERGE (japan1937:Steel {inYear: 1937, production: 580})
MERGE (japan)-[:PRODUCED]->(japan1937)
MERGE (japan1940:Steel {inYear: 1940, production: 686})
MERGE (japan)-[:PRODUCED]->(japan1940)
MERGE (japan1943:Steel {inYear: 1943, production: 765})
MERGE (japan)-[:PRODUCED]->(japan1943)

## Part 4 煤炭石油产量

## Part 5 GDP
// 创建 Economy 节点并建立关系
MERGE (germany:Country {name: "Germany"})
CREATE (economyGermany:Economy {GDP: 375, IndustrialOutput: 269, inYear: 1939})
MERGE (germany)-[:HAS_Economy]->(economyGermany);

MERGE (japan:Country {name: "Japan"})
CREATE (economyJapan:Economy {GDP: 169, IndustrialOutput: 70, inYear: 1939})
MERGE (japan)-[:HAS_Economy]->(economyJapan);

MERGE (italy:Country {name: "Italy"})
CREATE (economyItaly:Economy {GDP: 144, IndustrialOutput: 70, inYear: 1939})
MERGE (italy)-[:HAS_Economy]->(economyItaly);

MERGE (hungary:Country {name: "Hungary"})
CREATE (economyHungary:Economy {GDP: 14, IndustrialOutput: 6, inYear: 1939})
MERGE (hungary)-[:HAS_Economy]->(economyHungary);

MERGE (china:Country {name: "China"})
CREATE (economyChina:Economy {GDP: 320, IndustrialOutput: 30, inYear: 1939})
MERGE (china)-[:HAS_Economy]->(economyChina);

MERGE (sovietUnion:Country {name: "Soviet Union"})
CREATE (economySovietUnion:Economy {GDP: 417, IndustrialOutput: 250, inYear: 1939})
MERGE (sovietUnion)-[:HAS_Economy]->(economySovietUnion);

MERGE (unitedStates:Country {name: "United States"})
CREATE (economyUnitedStates:Economy {GDP: 1500, IndustrialOutput: 1000, inYear: 1939})
MERGE (unitedStates)-[:HAS_Economy]->(economyUnitedStates);

MERGE (britain:Country {name: "Britain"})
CREATE (economyBritain:Economy {GDP: 350, IndustrialOutput: 200, inYear: 1939})
MERGE (britain)-[:HAS_Economy]->(economyBritain);

MERGE (france:Country {name: "France"})
CREATE (economyFrance:Economy {GDP: 200, IndustrialOutput: 100, inYear: 1939})
MERGE (france)-[:HAS_Economy]->(economyFrance);

MERGE (poland:Country {name: "Poland"})
CREATE (economyPoland:Economy {GDP: 36, IndustrialOutput: 10, inYear: 1939})
MERGE (poland)-[:HAS_Economy]->(economyPoland);

## PART 6 军事力量


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
MERGE (russia:Country {name: "Soviet Union"})
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