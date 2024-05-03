"""
Cypher Query Snippets
"""

nodes_cypher = """
CALL apoc.load.json("file://nodes.json") YIELD value AS data
UNWIND data.nodes AS node
CALL apoc.merge.node([node.label], {name: node.name}, node.properties) YIELD node as n
RETURN count(n) AS nodesCreated
"""

relationships_cypher = """
CALL apoc.load.json("file://relations.json") YIELD value AS data
UNWIND data.relationships AS rel
MATCH (head {name: rel.start})
MATCH (tail {name: rel.end})
CALL apoc.create.relationship(head, rel.type, rel.properties, tail) YIELD rel as r
RETURN count(r) AS relationshipsCreated
"""
