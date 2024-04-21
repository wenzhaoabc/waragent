// MATCH (n) DETACH DELETE n

CREATE (a1:ActionType {name: 'Wait Without Action', input_type: 'country_list', input_type_desc: 'No', input_example: 'None', require_input: False, require_response: False, active: True, public: True, prerequisite: 'None', description: '(1) Wait for other countries responses and actions to decide further
(2) Will not exacerbate or improve the current situation, but sometimes when you to not have enough information, waiting is a prefered choice 
(3) Potentially lag behind other countries and put you in disadvantage
'});
CREATE (a2:ActionType {name: 'General Mobilization', input_type: 'country_list', input_type_desc: 'No', input_example: 'None', require_input: False, require_response: False, active: True, public: True, prerequisite: 'None', description: '(1) General mobilization typically refers to the process of preparing a nation\'s military and civilian resources for war, including conscripting soldiers, increasing production of military equipment, and implementing civil defense measures.
(2) Tensions will be escalated
(3) Other countries will be notified at once and may potentially choose to "Declare War" or "General Mobilization"
(4) Notice that it is dangerous not to "General Mobilization" if your potential enemies have already "General Mobilization"
'});
CREATE (a3:ActionType {name: 'Declare War', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country A", "Country B"]', require_input: True, require_response: True, active: True, public: True, prerequisite: 'None', description: '(1) Declare war against one specific country 
(2) Other countries, especially the allies of the target country and your enemies, will be alerted
(3) It is highly likely that your allies and enemies to  choose to "Declare War" and "General Mobilization" at once
(4) Notice that it is dangerous not to "Declare War" if your potential enemies have already "Declare War"
'});
CREATE (a4:ActionType {name: 'Request Military Alliance', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: True, active: True, public: False, prerequisite: 'None', description: '(1) Requesting military alliance can strengthen your power, which is good when feeling diplomatically or militarily isolated 
(2) The target country will be notified the alliance request and may choose to "Accept Military Alliance" or "Reject Military Alliance"
(3) You must consider whether this alliance may conflict interest with your current allies.
(4) It will only come to effect if the target country ACCEPT it; while target country may well REJECT.
'});
CREATE (a5:ActionType {name: 'Publish Military Alliance', input_type: 'country_tuple_list', input_type_desc: 'A two-dimensional list of strings, where each sublist is the names of other countries in your military alliance.', input_example: '[["Country P", "Country S"], ["Country M", "Country T", "Country U"]]', require_input: True, require_response: True, active: True, public: True, prerequisite: '(1) You can only Publish Military Alliance if you first "Request Military Alliance" and the target country chooses "Accept Military Alliance" from you.', description: '(1) Declare alliance with other countries will demonstrate strength and potentially deter other countries
'});
CREATE (a6:ActionType {name: 'Accept Military Alliance', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: False, public: False, prerequisite: 'None', description: '(1) Accepting military alliance means you will assist the target country/countries whenever they Declare War" against others or being attacked by others
(2) Accepting military alliance from the target country means you will also become an ally of other allies of the target country
(3) You should not ACCEPT military alliance simultaneously from two countries that are enemies to each other
'});
CREATE (a7:ActionType {name: 'Reject Military Alliance', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: False, public: False, prerequisite: 'None', description: '(1) Rejecting military alliance leads to either non-intervention treaty (if the other country send non-intervention treaty request) or state of hostile
'});
CREATE (a8:ActionType {name: 'Betray Military Alliance', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: True, public: False, prerequisite: '(1) You can only Betray Military Alliance if you and the target countries are indeed military alliance.', description: '(1) Betraying existent military alliance is a great offense to the target countries. The target countries may very likely to directly "Declare War" against you.
(2) After, betraying existent military alliance, you can choose to "Declare War" against them or maybe sign Non-Intervention Treaty with them to become neutral in their wars.
'});
CREATE (a9:ActionType {name: 'Request Non-Intervention Treaty', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X, "Country Y", "Country Z"]', require_input: True, require_response: True, active: True, public: False, prerequisite: 'None', description: '(1) Asking the target countries commit not to help your enemies in military conflicts or wars, i.e. they will be neutral.
It will only come to effect if the target country ACCEPT it; while target country may well REJECT.
So if you declare war on other countries, countries who ACCEPT this non-intervention treaty would not be allowed to assist the country that has been declared war upon. 
(2) ACCEPTTed and effective non-intervention Treaty can lower your risk when declaring wars 
(3) ACCEPTTed and effective non-intervention Treaty may lower threatens from other countries 
'});
CREATE (a10:ActionType {name: 'Reject Non-Intervention Treaty', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: False, public: False, prerequisite: 'None', description: '(1) Rejecting non-intervention treaty from the target countries leads directly to state of hostile against the target countries 
(2) Rejecting non-intervention treaty from the target countries basically means you will "Declare War" against the target country in the future if necessary
'});
CREATE (a11:ActionType {name: 'Accept Non-Intervention Treaty', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: False, public: False, prerequisite: 'None', description: '(1) Accepting non-intervention treaty from the target countries means that you will not intervene in any war or military actions performed by the target country. 
(2) Breaking the accepted non-intervention treaty from the target countries will let all other countries to lose trust on you and be more hostile against you.
(3) You should not ACCEPT non-intervention treaty simultaneously from two countries that are enemies to each other
'});
CREATE (a12:ActionType {name: 'Publish Non-Intervention Treaty', input_type: 'country_tuple_list', input_type_desc: 'A two-dimensional list of strings, where each sublist is the names of other countries in your non-intervention treaty group.', input_example: '[["Country P"], ["Country M", "Country T", "Country U"]]', require_input: True, require_response: False, active: True, public: True, prerequisite: '(1)You can only Publish Non-intervention Treaty Information if you first "Request Non-InterventionTreaty" and the target country chooses "Accept Non-Intervention Treaty" from you.', description: '(1) Publishing Non-intervention Treaty with participating countries will caution others to be aware that alliance with the participating countries against you is impossible 
(2) Publishing non-intervention Treaty can lower your risk when declaring wars (3) Publishing non-intervention Treaty may lower the probability of being betrayed from the target country, as the cost of breaking promise is higher now, but there\'s still probability
'});
CREATE (a13:ActionType {name: 'Betray Non-Intervention Treaty', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: True, public: False, prerequisite: '(1) You can only Betray Non-Intervention Treaty if you and the target countries have signed non-intervention treaty. ', description: '(1) Betraying existent military alliance is a great offense to the target countries. The target countries may very likely to directly "Declare War" against you.
(2) After betraying existent Non-Intervention Treaty, you should "Declare War" against the target countries.
'});
CREATE (a14:ActionType {name: 'Present Peace Agreement', input_type: 'country_dict', input_type_desc: 'A list of key-value pairs, where the key is the name of the country in the peace agreement, and the content attribute of the value is the content of the peace agreement.', input_example: '[{"Country A":{"content":"We hereby commit to entering into a peace treaty with you, contingent upon our allocation of two strategically significant naval ports."}},{"Country B":{"content":"The content of the peace agreement with Country B"}}]', require_input: True, require_response: False, active: True, public: True, prerequisite: 'None', description: '(1) You only present peace agreement if you are scared of war and been defeated by the target country, thus request peace 
(2) The target country will receive the agreement contents. It will only come to effect if the target country ACCEPT it; but it may well REJECT it.
'});
CREATE (a15:ActionType {name: 'Accept Peace Agreement', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: False, public: True, prerequisite: 'None', description: '(1) If you Accept the Peace Agreement, then you should act following the content and never {Declare_War} against the target country.'});
CREATE (a16:ActionType {name: 'Reject Peace Agreement', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: False, public: True, prerequisite: 'None', description: '(1) The country presenting the agreement may be provoked to choose "Declare War" or "General Mobilization"
(2) the country presenting the agreement may revise agreement content and choose {Present_Peace_Agreement} again
'});
CREATE (a17:ActionType {name: 'Publish Peace Agreement', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: True, public: True, prerequisite: '(1) You can only Publish Peace Agreement if you first "Present Peace Agreement" and the target country chooses "Accept Peace Agreement" from you, or you "Accept Peace Agreement" presented from some country.', description: '(1) Publish Peace Agreement to all other countries indicate that you shall never choose to "Declare War" against the country/countries that you sign the agreement with.
'});
CREATE (a18:ActionType {name: 'Betray Peace Agreement', input_type: 'country_list', input_type_desc: 'list of target country name(s)', input_example: '["Country X", "Country Y", "Country Z"]', require_input: True, require_response: False, active: True, public: False, prerequisite: '(1) You can only Betray Peace Agreement if you and the target countries have signed peace agreement.', description: '(1) Betraying existent Peace_Agreement is a great offense to the target countries. The target countries may very likely to directly "Declare War" against you.
(2) After betraying existent Peace_Agreement, you should "Declare War" against the target countries.
'});
CREATE (a19:ActionType {name: 'Send Message', input_type: 'country_dict', input_type_desc: 'A dictionary with the country name as the key and the content of the message as the value\'s content attribute.', input_example: '{"Country A":{"content":"The content of the message to Country A"},"Country B":{"content":"The content of the message to Country B"}}', require_input: True, require_response: True, active: True, public: False, prerequisite: 'None', description: '(1) Send message to other countries to communicate with them'});


MATCH(a: ActionType {name: 'Present Peace Agreement'})
MATCH(b: ActionType {name: 'Accept Peace Agreement'})
MATCH(c: ActionType {name: 'Reject Peace Agreement'})
MATCH(d: ActionType {name: 'Publish Peace Agreement'})
MATCH(e: ActionType {name: 'Betray Peace Agreement'})
MERGE (b)-[:PREREQUISITE]->(a)
MERGE (c)-[:PREREQUISITE]->(a)
MERGE (d)-[:PREREQUISITE]->(b)
MERGE (e)-[:PREREQUISITE]->(b)


MATCH(a: ActionType {name: 'Request Non-Intervention Treaty'})
MATCH(b: ActionType {name: 'Accept Non-Intervention Treaty'})
MATCH(c: ActionType {name: 'Reject Non-Intervention Treaty'})
MATCH(d: ActionType {name: 'Publish Non-Intervention Treaty'})
MATCH(e: ActionType {name: 'Betray Non-Intervention Treaty'})
MERGE (b)-[:PREREQUISITE]->(a)
MERGE (c)-[:PREREQUISITE]->(a)
MERGE (d)-[:PREREQUISITE]->(b)
MERGE (e)-[:PREREQUISITE]->(b)

MATCH(a: ActionType {name: 'Request Military Alliance'})
MATCH(b: ActionType {name: 'Accept Military Alliance'})
MATCH(c: ActionType {name: 'Reject Military Alliance'})
MATCH(d: ActionType {name: 'Publish Military Alliance'})
MATCH(e: ActionType {name: 'Betray Military Alliance'})
MERGE (b)-[:PREREQUISITE]->(a)
MERGE (c)-[:PREREQUISITE]->(a)
MERGE (d)-[:PREREQUISITE]->(b)
MERGE (e)-[:PREREQUISITE]->(b)
