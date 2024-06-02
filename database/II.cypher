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


## PART 7 1939年经济状况

// 创建国家节点
MERGE (germany:Country {name: "Germany"})

// 创建GDP节点并与德国关联
MERGE (gdp:GDP {value: 209000000000, year: 1939})
MERGE (germany)-[:HAS_GDP]->(gdp)

// 创建政府收入节点并与德国关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (germany)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {source: 'Middle class and wealthy'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {type: 'War bonds'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Limited external aid'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与德国关联
MERGE (militaryExpenditure:MilitaryExpenditure {percentageOfGDP: 20, year: 1939})
MERGE (germany)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与德国关联
MERGE (socialWelfare:SocialWelfare {description: 'Limited benefits'})
MERGE (reconstruction:Reconstruction {status: 'Not applicable'})
MERGE (germany)-[:HAS_WELFARE]->(socialWelfare)
MERGE (germany)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与德国关联
MERGE (internationalTrade:InternationalTrade {description: 'Raw materials and military goods'})
MERGE (germany)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Increasing, especially in military goods'})
MERGE (importVolumes:ImportVolumes {description: 'Key commodities like oil'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

----- 日本 -----

// 创建国家节点
MERGE (japan:Country {name: "Japan"})

// 创建政府收入节点并与日本关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (japan)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {system: 'Progressive', types: ['Income', 'Inheritance', 'Consumption']})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {type: 'War bonds', purpose: 'Military operations'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Minimal aid'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与日本关联
MERGE (militaryExpenditure:MilitaryExpenditure {percentageOfBudget: '25-30%', year: 1939})
MERGE (japan)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与日本关联
MERGE (socialWelfare:SocialWelfare {description: 'Limited programs, focus on war efforts'})
MERGE (reconstruction:Reconstruction {status: 'Not applicable'})
MERGE (japan)-[:HAS_WELFARE]->(socialWelfare)
MERGE (japan)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与日本关联
MERGE (internationalTrade:InternationalTrade {description: 'Raw materials, textiles, manufactured goods'})
MERGE (japan)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Raw materials, textiles, manufactured goods'})
MERGE (importVolumes:ImportVolumes {description: 'Oil, raw materials, machinery'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

---- 意大利 -----

// 创建国家节点
MERGE (italy:Country {name: "Italy"})

// 创建政府收入节点并与意大利关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (italy)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {description: 'High taxation', regime: 'Fascist'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {type: 'War bonds', purpose: 'Military ambitions'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Limited aid from Germany'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与意大利关联
MERGE (militaryExpenditure:MilitaryExpenditure {description: 'Significant portion of budget', year: 1939})
MERGE (italy)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与意大利关联
MERGE (socialWelfare:SocialWelfare {description: 'Some programs, resources redirected to military'})
MERGE (reconstruction:Reconstruction {status: 'Not applicable'})
MERGE (italy)-[:HAS_WELFARE]->(socialWelfare)
MERGE (italy)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与意大利关联
MERGE (internationalTrade:InternationalTrade {description: 'Textiles, machinery, vehicles'})
MERGE (italy)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Textiles, machinery, vehicles'})
MERGE (importVolumes:ImportVolumes {description: 'Oil, iron ore'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...


---- 匈牙利 ----

// 创建国家节点
MERGE (hungary:Country {name: "Hungary"})

// 创建政府收入节点并与匈牙利关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (hungary)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {system: 'Progressive income tax system'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {type: 'War bonds', purpose: 'Military build-up'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Economic assistance from Germany'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与匈牙利关联
MERGE (militaryExpenditure:MilitaryExpenditure {description: 'Increased significantly before the war', year: 1939})
MERGE (hungary)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与匈牙利关联
MERGE (socialWelfare:SocialWelfare {description: 'Limited programs, minimal compared to war effort'})
MERGE (reconstruction:Reconstruction {status: 'Not applicable'})
MERGE (hungary)-[:HAS_WELFARE]->(socialWelfare)
MERGE (hungary)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与匈牙利关联
MERGE (internationalTrade:InternationalTrade {description: 'Agricultural products, machinery, textiles'})
MERGE (hungary)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Agricultural products, machinery, textiles'})
MERGE (importVolumes:ImportVolumes {description: 'Raw materials like oil and steel'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

---- 中国 -----

// 创建国家节点
MERGE (china:Country {name: "China"})

// 创建政府收入节点并与中国关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (china)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {description: 'Primarily levied on land, customs duties, and excise taxes'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {description: 'War bonds to finance war efforts against Japan'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Limited aid from Western powers and the Soviet Union'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与中国关联
MERGE (militaryExpenditure:MilitaryExpenditure {description: 'Increased significantly due to the ongoing war with Japan', year: 1939})
MERGE (china)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与中国关联
MERGE (socialWelfare:SocialWelfare {description: 'Limited resources allocated for welfare, focused on supporting soldiers and their families'})
MERGE (reconstruction:Reconstruction {status: 'No significant post-war reconstruction spending'})
MERGE (china)-[:HAS_WELFARE]->(socialWelfare)
MERGE (china)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与中国关联
MERGE (internationalTrade:InternationalTrade {description: 'Trade suffered due to the war'})
MERGE (china)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Exports affected by Japanese control over key ports'})
MERGE (importVolumes:ImportVolumes {description: 'Essential materials like oil, steel, and weapons'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

----- 苏联 ----

// 创建国家节点
MERGE (ussr:Country {name: "Soviet Union"})

// 创建政府收入节点并与苏联关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (ussr)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {system: 'Centralized state enterprises'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {type: 'Minimal foreign debt'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Minimal, non-alignment policy'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与苏联关联
MERGE (militaryExpenditure:MilitaryExpenditure {description: 'Substantial, modernizing and expanding armed forces', year: 1939})
MERGE (ussr)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与苏联关联
MERGE (socialWelfare:SocialWelfare {description: 'Basic social safety net, limited compared to Western standards'})
MERGE (reconstruction:Reconstruction {status: 'Not applicable'})
MERGE (ussr)-[:HAS_WELFARE]->(socialWelfare)
MERGE (ussr)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与苏联关联
MERGE (internationalTrade:InternationalTrade {description: 'Significant exporter of raw materials'})
MERGE (ussr)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Raw materials and imports of machinery and technology'})
MERGE (importVolumes:ImportVolumes {description: 'Technology, machinery, and oil'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

----- 美国 ---- 

// 创建国家节点
MERGE (usa:Country {name: "United States"})


// 创建政府收入节点并与美国关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (usa)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {description: 'Income taxes were the primary source'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {amount: 20000000000, year: 1939})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Limited aid under the Lend-Lease Act'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与美国关联
MERGE (militaryExpenditure:MilitaryExpenditure {amount: 1700000000, year: 1939})
MERGE (usa)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与美国关联
MERGE (socialWelfare:SocialWelfare {description: 'Programs like Social Security were established'})
MERGE (reconstruction:Reconstruction {status: 'Not significant'})
MERGE (usa)-[:HAS_WELFARE]->(socialWelfare)
MERGE (usa)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与美国关联
MERGE (internationalTrade:InternationalTrade {description: 'Major trading nation'})
MERGE (usa)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Exported goods worth $4.5 billion'})
MERGE (importVolumes:ImportVolumes {description: 'Imported goods worth $4.2 billion'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

---- 英国 ----

// 创建国家节点
MERGE (uk:Country {name: "United Kingdom"})

// 创建政府收入节点并与英国关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (uk)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {description: 'Income tax, inheritance tax, customs duties'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {amount: 6700000000, year: 1939})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Later aid from the U.S. through Lend-Lease Act'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与英国关联
MERGE (militaryExpenditure:MilitaryExpenditure {amount: 1100000000, year: 1939})
MERGE (uk)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与英国关联
MERGE (socialWelfare:SocialWelfare {description: 'Pensions, unemployment benefits'})
MERGE (reconstruction:Reconstruction {status: 'Not a major priority yet'})
MERGE (uk)-[:HAS_WELFARE]->(socialWelfare)
MERGE (uk)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与英国关联
MERGE (internationalTrade:InternationalTrade {description: 'Trade disrupted by the war'})
MERGE (uk)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Exports disrupted by German U-boat attacks'})
MERGE (importVolumes:ImportVolumes {description: 'Oil from the Middle East, raw materials from colonies'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

---- 法国 ----

// 创建国家节点
MERGE (france:Country {name: "France"})

// 创建政府收入节点并与法国关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (france)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {system: 'Progressive income tax system'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {amount: 1500000000000, year: 1939})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'Support from the UK'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与法国关联
MERGE (militaryExpenditure:MilitaryExpenditure {amount: 12000000000, year: 1939})
MERGE (france)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与法国关联
MERGE (socialWelfare:SocialWelfare {description: 'Social security system'})
MERGE (reconstruction:Reconstruction {status: 'Not applicable'})
MERGE (france)-[:HAS_WELFARE]->(socialWelfare)
MERGE (france)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与法国关联
MERGE (internationalTrade:InternationalTrade {description: 'Major trading nation'})
MERGE (france)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Textiles, machinery, luxury items'})
MERGE (importVolumes:ImportVolumes {description: 'Raw materials, foodstuffs'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

---- 波兰 ----

// 创建国家节点
MERGE (poland:Country {name: "Poland"})

// 创建政府收入节点并与波兰关联
MERGE (governmentRevenue:GovernmentRevenue {year: 1939})
MERGE (poland)-[:HAS_REVENUE]->(governmentRevenue)

// 创建税收、债务发行、外国援助和贷款节点，并与政府收入关联
MERGE (taxes:Taxes {description: 'Customs duties, excise taxes, income taxes'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(taxes)

MERGE (nationalDebt:NationalDebt {type: 'War bonds', year: 1939})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(nationalDebt)

MERGE (foreignAid:ForeignAid {description: 'From France and the United Kingdom'})
MERGE (governmentRevenue)-[:SOURCE_INCLUDES]->(foreignAid)

// 创建军事支出节点，并与波兰关联
MERGE (militaryExpenditure:MilitaryExpenditure {percentageOfGDP: '10%', year: 1939})
MERGE (poland)-[:HAS_EXPENDITURE]->(militaryExpenditure)

// 创建社会福利和重建支出节点，并与波兰关联
MERGE (socialWelfare:SocialWelfare {description: 'Limited resources allocated to welfare programs'})
MERGE (reconstruction:Reconstruction {status: 'Not applicable'})
MERGE (poland)-[:HAS_WELFARE]->(socialWelfare)
MERGE (poland)-[:HAS_RECONSTRUCTION]->(reconstruction)

// ... 其他节点和关系的创建类似上面的模式 ...

// 例如，创建国际交易节点并与波兰关联
MERGE (internationalTrade:InternationalTrade {description: 'Agricultural and industrial exporter'})
MERGE (poland)-[:HAS_TRADE]->(internationalTrade)

// 创建出口和进口量节点，并与国际交易关联
MERGE (exportVolumes:ExportVolumes {description: 'Agricultural and industrial goods'})
MERGE (importVolumes:ImportVolumes {description: 'Oil and raw materials'})
MERGE (internationalTrade)-[:INCLUDES]->(exportVolumes)
MERGE (internationalTrade)-[:INCLUDES]->(importVolumes)

// ... 继续添加其他节点和关系 ...

