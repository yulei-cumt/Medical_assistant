from py2neo import Graph
graph = Graph("http://localhost:7474", auth=("neo4j", "UCAS251340"))
try:
    graph.run("Match () Return 1 Limit 1")
    print('The database connection is normal.')
except Exception:
    print('Error.')



