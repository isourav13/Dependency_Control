import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv

# Create a directed graph
G = nx.DiGraph()

# Define nodes and their hierarchical relationships with probabilities
nodes = {
    "Queries": {"Read Queries": 0.4, "Write Queries": 0.3, "Search Queries": 0.3},
    "Read Queries": {"Simple Reads": 0.3, "Complex Reads": 0.4, "Filtered Reads": 0.2, "Aggregations": 0.1, "Joins": 0.2},
    "Filtered Reads": {"Range Queries": 0.5, "Multi-attribute Filters": 0.5},
    "Aggregations": {"Count": 0.4, "Sum": 0.3, "Min/Max": 0.3},
    "Joins": {"Inner Joins": 0.6, "Left Joins": 0.1, "Right Joins": 0.1, "Full Joins": 0.2},
    "Write Queries": {"Create": 0.4, "Update": 0.3, "Delete": 0.2, "Upsert": 0.1},
    "Create": {"Single Create": 0.6, "Bulk Create": 0.4},
    "Update": {"Full Update": 0.4, "Partial Update (Patch)": 0.4, "Bulk Update": 0.2},
    "Delete": {"Soft Delete": 0.5, "Hard Delete": 0.5}
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

# Add edges with probabilities to the graph
for parent, children in nodes.items():
    for child, prob in children.items():
        G.add_edge(parent, child, label=f"{prob:.1f}")

# Create a pygraphviz AGraph from the NetworkX graph for better layout
G_pg = nx.nx_agraph.to_agraph(G)
G_pg.graph_attr.update(rankdir="LR")  # Set the layout direction to left-to-right
G_pg.node_attr.update(style="filled", fontsize=20)  # Increase font size for nodes
G_pg.edge_attr.update(fontsize=16)  # Increase font size for edge labels

# Set node colors
for node in G_pg.nodes():
    node.attr['fillcolor'] = colors.get(node, "white")

# Draw the graph
plt.figure(figsize=(30, 20))  # Adjust figsize to accommodate left-to-right layout
G_pg.layout(prog="dot")  # Use 'dot' layout algorithm for hierarchical graphs
G_pg.draw(path="horizontal_graph_with_probs.png", format="png")

