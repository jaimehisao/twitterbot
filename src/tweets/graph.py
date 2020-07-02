import networkx as nx
import matplotlib.pyplot as plt

import psycopg2

g = nx.Graph()

print(g.nodes())
print(g.edges())

# adding just one node:
g.add_node("a")
# a list of nodes:
g.add_nodes_from(["b", "c"])

print(g.nodes())
print(g.edges())

g.add_edge(1, 2)
edge = ("d", "e")
g.add_edge(*edge)
edge = ("a", "b")
g.add_edge(*edge)

print("Nodes of graph: ")
print(g.nodes())
print("Edges of graph: ")
print(g.edges())

# adding a list of edges:
g.add_edges_from([("a", "c"), ("c", "d"), ("a", 1), (1, "d"), ("a", 2)])

nx.draw(g)
# plt.savefig("simple_path.png") # save as png
plt.show()  # display

G = nx.path_graph(4)

print(nx.info(g))

# Path graph
print("Nodes of graph: ")
print(G.nodes())
print("Edges of graph: ")
print(G.edges())
nx.draw(G)
plt.savefig("path_graph1.png")
plt.show()
