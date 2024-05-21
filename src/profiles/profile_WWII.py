from src.profiles.agent_profile import CountryProfile

"""
Countries in WWII
Germany
Japan
Italy

United States
Soviet Union
United Kingdom
China
France
"""

# 德国
Germany = CountryProfile(
    real_name="Germany",
    country_name="Country GE",
    leader_ship="(1) A totalitarian state under a fascist regime, led by a dictator with an ideology centered on nationalism and militarism.",
    military_capability="(1) Standing army population: Over 18 million soldiers throughout the war \n(2) Advanced military technology including tanks, aircraft, and rockets, notable for blitzkrieg tactics \n(3) Naval tonnage: 14.4 million, significant submarine fleet used for disrupting Allied supply lines",
    natural_industry_resource="(1) Rich in natural resources such as coal, iron, and other minerals \n(2) Industrial capacity: Germany was a leading industrial power in the 1930s, with a strong manufacturing base for weapons and machinery",
    history_background="(1) Legacy of World War I: Treaty of Versailles imposed harsh conditions on Germany, leading to economic hardship and resentment",
    key_policy="(1) Lebensraum: Expansionist policy to secure living space for the German people",
    public_morale="(1) Strong propaganda machine promoting nationalism and anti-Semitism \n(2) Initial public support",
)

# 日本
Japan = CountryProfile(
    real_name="Japan",
    country_name="Country JA",
    leader_ship="(1) A militaristic state under an emperor with a government dominated by military leaders",
    military_capability="(1) Standing army population: Over 6 million soldiers throughout the war \n(2) Advanced military technology including aircraft carriers, submarines, and kamikaze tactics \n(3) Naval tonnage: 2.1 million, significant naval power in the Pacific",
    natural_industry_resource="(1) Limited natural resources, heavily reliant on imports for raw materials \n(2) Industrial capacity: Japan had a strong industrial base for shipbuilding and electronics",
    history_background="(1) Expansionist policies in Asia, including the invasion of Manchuria and China",
    key_policy="(1) Greater East Asia Co-Prosperity Sphere: Vision of a united Asia under Japanese control",
    public_morale="(1) Strong nationalist sentiment and loyalty to the emperor \n(2) Initial public support",
)

# 意大利
Italy = CountryProfile(
    real_name="Italy",
    country_name="Country IT",
    leader_ship="(1) Fascist dictatorship under a single leader, marked by authoritarianism and a push for national prestige and expansion",
    military_capability=f"(1) Standing army population: Approximately 0.45 million soldiers.\n"
    f"(2) Naval tonnage: 0.7 million, facing challenges in modernization and resource allocation.\n"
    f"(3) Air force with limited capacity compared to major powers of the era.",
    natural_industry_resource=f"(1) Geography: has long coastline\n"
    f"(2) Population: Around 44 million\n"
    f"(3) GDP: Faced economic challenges, with efforts directed towards militarization and war\n"
    f"(4) Terrain: Diverse, including coastal plains, mountainous regions, and fertile river valleys\n"
    f"(5) Weather: Predominantly warm climate, with regional variations",
    history_background=f"(1) dissatisfaction from previous war led to the rise of fascism in society (2) One of the oldest country in the world who was once the dominance in the world but no more.",
    key_policy=f"(1) Expansionist and imperialist policies aimed at establishing a new Empire to revive the old glory\n"
    f"(2) Increase influence in other areas in the world",
    public_morale="(1) Mixed, with initial support for the regime's ambitions, but declining significantly due to military setbacks and the realities of war.",
)

# 匈牙利
Hungary = CountryProfile(
    real_name="Hungary",
    country_name="Country HU",
    leader_ship="(1) Governed by a regency with authoritarian tendencies, influenced by both fascist and conservative elements",
    military_capability="(1) Standing army population: Approximately 0.4 million soldiers.\n"
    "(2) Limited military modernization and resources compared to major powers",
    natural_industry_resource="(1) Geography: Landlocked country.\n"
    "(2) Population: About 9 million.\n"
    "(3) GDP: Moderate, with an economy struggling and recession.\n"
    "(4) Terrain: Dominated by the Great Hungarian Plain, with mountainous regions to the north.\n"
    "(5) Weather: Continental climate, with hot summers and cold winters",
    history_background="(1) Post-war territorial losses influenced its alliance choices",
    key_policy="(1) Aimed at territorial expansion.\n"
    "(2) Initially allied with Country GE and Country IT, but later attempted to negotiate a separate peace as the war turned against them.",
    public_morale="(1) Public morale varied, initially supportive of territorial gains but also careful due to previous war losses and economic hardship",
)

United_States = CountryProfile(
    real_name="United States",
    country_name="Country US",
    leader_ship="(1) A democratic federal republic with leadership emphasizing freedom and democracy, rallying the nation in a unified war effort",
    military_capability=(
        "(1) Standing army population: Grew to over 17.8 million soldiers\n"
        "(2) Naval tonnage: 4.63 million, becoming one of the largest in the world\n"
        "(3) Air force capabilities: Developed one of the most powerful air forces, with significant advancements in aircraft technology"
    ),
    natural_industry_resource=(
        "(1) Geography: Large country with diverse landscapes\n"
        "(2) Population: About 140 million\n"
        "(3) GDP: Massive industrial output.\n"
        "(4) Terrain: Varies from plains and mountains to forests and coastlines\n"
        "(5) Weather: Diverse, ranging from temperate to tropical climates"
    ),
    history_background=(
        "(1) Country US is a  very young country.\n"
        "(2) Traditionally being a country with isolating policy, but benefit greatly from previous winning war  "
    ),
    key_policy=(
        "(1) Focused on total war effort, mobilizing military and civilian resources for victory\n"
        "(2) Key policies included develop nuclear weapons"
    ),
    public_morale="(1) Public morale was high, marked by a strong sense of unity and purpose, boosted by effective propaganda and a shared sense of fighting for democracy and freedom",
)

Soviet_Union = CountryProfile(
    real_name="Soviet Union",
    country_name="Country SU",
    leader_ship="(1) A totalitarian regime under a communist government, characterized by centralized control and a single-party state",
    military_capability=(
        "(1) Standing army population: Over 34 million soldiers throughout the war.\n"
        "(2) Naval tonnage: 0.4 million. Large tank forces and significant artillery capabilities.\n"
        "(3) Renowned for the harsh winter warfare."
    ),
    natural_industry_resource=(
        "(1) Geography: Vast country but mostly landlocked.\n"
        "(2) Population: Approximately 170 million.\n"
        "(3) GDP: Large-scale industrialization efforts, particularly in armaments.\n"
        "(4) Terrain: Diverse, ranging from steppes in the south to dense forests and tundra in the north.\n"
        "(5) Weather: Extremes of climate, especially severe winters"
    ),
    history_background="(1) Suffered massive human and material losses during previous war",
    key_policy=(
        "(1) Focused on a strategy of scorched earth to deny resources to the invading forces.\n"
        "(2) Mobilization of the entire nation for war effort"
    ),
    public_morale="(1) Characterized by resilience and sacrifice, with a strong sense of defending the motherland against invaders",
)

Britain = CountryProfile(
    real_name="Britain",
    country_name="Country BR",
    leader_ship="(1) A constitutional monarchy with significant democratic institutions, characterized by the pragmatic and stoic leadership of Winston Churchill during the war period",
    military_capability=(
        "(1) Standing army population: Approximately 5.5 million soldiers.\n"
        "(2) Naval tonnage: 1.3 million, critical in maintaining supply routes and blockading Axis powers.\n"
        "(3) Extensive air force capabilities, crucial in the Battle of Country BR and strategic bombing campaigns."
    ),
    natural_industry_resource=(
        "(1) Geography: Island nation, strategically positioned to control key shipping lanes.\n"
        "(2) Population: About 48 million.\n"
        "(3) GDP: Focused on war effort, with extensive industrial and colonial resources.\n"
        "(4) Terrain: Varied, including rolling hills, highlands, and urban areas.\n"
        "(5) Weather: Generally mild and maritime, playing a role in military operations"
    ),
    history_background=(
        "(1) It was once the strongest country in the world, but now surpassed by Country US.\n"
        "(2) Although it was never defeated in wars, it has sacrificed a great number of population and labor force in previous wars."
    ),
    key_policy=(
        "(1) Maintained a policy of total war, mobilizing all national resources for the war effort.\n"
        "(2) Strong focus on international alliances and coordination with other potential allies"
    ),
    public_morale="(1) High public morale, bolstered by widespread support for the war effort and the leadership of the President, with a spirit of resilience and determination",
)

China = CountryProfile(
    real_name="China",
    country_name="Country CH",
    leader_ship="(1) A coalition government led by two parties with contradictory ideologies",
    military_capability=(
        "(1) Standing army population: Over 5 millions serving over the course of the war.\n"
        "(2) Naval tonnage: 0.03 million. Lacked modern equipment and training compared to Japan, relying on guerilla tactics and Allied support.\n"
        "(3) Suffered from logistical difficulties and internal disunity"
    ),
    natural_industry_resource=(
        "(1) Geography: Vast country with diverse landscapes, including mountains, rivers, and coastlines.\n"
        "(2) Population: Over 500 million.\n"
        "(3) GDP: Economically strained due to prolonged warfare and occupation.\n"
        "(4) Terrain: Ranging from the Himalayas in the west to coastal plains in the east.\n"
        "(5) Weather: Varies from subtropical to temperate, with regional differences affecting military operations"
    ),
    history_background="(1) Faced prolonged conflict with Country JA invasion.",
    key_policy=(
        "(1) Primary focus on resisting Country JA's aggression and maintaining national sovereignty.\n"
        "(2) Sought international support and collaboration, particularly with the Country US"
    ),
    public_morale="(1) Public morale was a complex mix of resilience in the face of invasion, suffering due to war atrocities, and hope for eventual liberation ",
)

France = CountryProfile(
    real_name="France",
    country_name="Country FR",
    leader_ship="(1) A democratic republic",
    military_capability=(
        "(1) Standing army population: 0.15 million.\n"
        "(2) Naval tonnage: 0.17 million."
    ),
    natural_industry_resource=(
        "(1) Geography: medium size country with a varied landscape including coastal areas, plains, and mountains.\n"
        "(2) Population: Approximately 42 million.\n"
        "(3) GDP: Suffered economically from previous war and global economic recession.\n"
        "(4) Terrain: Includes both agricultural regions and industrial centers.\n"
        "(5) Weather: Generally temperate, with regional variations"
    ),
    history_background="(1) Facing threaten from Country GE.",
    key_policy=(
        "(1) The Vichy regime sought to collaborate with Country GE while maintaining some autonomy.\n"
        "(2) The Free Country FR Forces and the Resistance aimed to liberate Country FR"
    ),
    public_morale="(1) Initially shocked and demoralized by the rapid defeat, but the spirit of resistance and hope for liberation grew, especially after the Allied landings in Normandy.",
)

# 波兰
Poland = CountryProfile(
    real_name="Poland",
    country_name="Country PO",
    leader_ship="(1) Democratic republic with a parliamentary system. Transitioning toward an authoritarian regime under increased pressure from internal and external threats.",
    military_capability=(
        "(1) Standing army population: Approximately 1.35 million soldiers.\n"
        "(2) Military equipment includes a mix of modern and outdated weaponry.\n"
        "(3) Strong emphasis on cavalry and mechanized infantry."
    ),
    natural_industry_resource=(
        "(1) Geography: Located in Central Europe, with a mix of plains, forests, and mountains to the south.\n"
        "(2) Population: Over 35 million.\n"
        "(3) GDP: Modest, with a predominantly agrarian economy but with industrialized sectors in major cities.\n"
        "(4) Terrain: Generally flat with some mountainous regions to the south.\n"
        "(5) Weather: Continental climate, with cold winters and warm summers."
    ),
    history_background=(
        "(1) Regained independence in recent years after over a century of partition.\n"
        "(2) A history of conflict with neighboring countries and struggles for sovereignty."
    ),
    key_policy=(
        "(1) Focused on maintaining sovereignty and territorial integrity.\n"
        "(2) Sought to form alliances with other countries to counter potential threats from Country JA and Country US.\n"
        "(3) Emphasized national unity and defense preparedness."
    ),
    public_morale=(
        "(1) Strong sense of nationalism and resilience due to a history of foreign occupation and resistance.\n"
        "(2) Public morale high in the face of threats, with a deep-rooted sense of identity and commitment to independence."
    ),
)

CountryProfileList = [
    Germany,
    Japan,
    Italy,
    Hungary,
    China,
    Soviet_Union,
    United_States,
    Britain,
    France,
    Poland,
]

# print(Germany)
# print(len(CountryProfileList))
# for c in CountryProfileList:
#     print(c.country_name)
# for country in CountryProfileList:
#     print(country)

# fake_real_name = {}
# for country in CountryProfileList:
#     fake_real_name[country.country_name] = country.real_name

# s = ""
# for country in CountryProfileList:
#     s += country.__str__()
#     s += "\n===================\n"

# for f, r in fake_real_name.items():
#     s = s.replace(f, r)

# print(s)
