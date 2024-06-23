import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv

# Create a directed graph
G = nx.DiGraph()

# Define nodes and their hierarchical relationships
nodes = {
    "Queries": ["Read Queries", "Write Queries", "Search Queries", "Transactional Queries", "Caching Queries"],
    "Read Queries": ["Simple Reads", "Complex Reads", "Filtered Reads", "Aggregations", "Joins"],
    "Filtered Reads": ["Range Queries", "Multi-attribute Filters"],
    "Aggregations": ["Count", "Sum", "Min/Max"],
    "Joins": ["Inner Joins", "Left Joins", "Right Joins", "Full Joins"],
    "Write Queries": ["Create", "Update", "Delete", "Upsert"],
    "Create": ["Single Create", "Bulk Create"],
    "Update": ["Full Update", "Partial Update (Patch)", "Bulk Update"],
    "Delete": ["Soft Delete", "Hard Delete"]
}

# Define node colors
colors = {
    "Queries": "lightblue",
    "Read Queries": "lightgreen",
    "Write Queries": "lightcoral",
    "Transactional Queries": "lightgoldenrodyellow",
    "Caching Queries": "lightpink",
    "Search Queries": "lightseagreen"
}

# Add edges to the graph
for parent, children in nodes.items():
    for child in children:
        G.add_edge(parent, child)

# Draw the graph with better layout using pygraphviz
plt.figure(figsize=(20, 15))

# Create a pygraphviz AGraph from the NetworkX graph for better layout
G_pg = nx.nx_agraph.to_agraph(G)
G_pg.layout(prog="dot")  # Use 'dot' layout algorithm for hierarchical graphs

# Draw nodes and edges
node_colors = [colors.get(node, "white") for node in G.nodes]
G_pg.draw(path="high_res_graph.png", format="png", prog="dot")

# Display the graph (optional, if you want to display in a notebook)
plt.title("Queries in Microservices Tree Structure")
plt.imshow(plt.imread("graph.png"))
plt.axis("off")
#plt.show()
#end



