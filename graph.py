import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Define nodes and their hierarchical relationships
nodes = {
    "Queries in Microservices": ["Read Queries", "Write Queries", "Transactional Queries", "Caching Queries", "Search Queries"],
    "Read Queries": ["Simple Reads", "Complex Reads"],
    "Simple Reads": ["Get by ID", "Get All", "Get by Attribute"],
    "Complex Reads": ["Filtered Reads", "Aggregations", "Joins"],
    "Filtered Reads": ["Range Queries", "Multi-attribute Filters"],
    "Aggregations": ["Count", "Sum", "Average", "Min/Max"],
    "Joins": ["Inner Joins", "Left Joins", "Right Joins", "Full Joins"],
    "Write Queries": ["Create", "Update", "Delete", "Upsert"],
    "Create": ["Single Create", "Bulk Create"],
    "Update": ["Full Update", "Partial Update (Patch)", "Bulk Update"],
    "Delete": ["Soft Delete", "Hard Delete"],
    "Transactional Queries": ["Distributed Transactions", "Single Microservice Transactions"],
    "Distributed Transactions": ["Two-Phase Commit", "Saga Pattern"],
    "Caching Queries": ["Cache Read", "Cache Write", "Cache Invalidate"],
    "Search Queries": ["Full-Text Search", "Fuzzy Search", "Geospatial Search", "Custom Search Queries"]
}

# Add edges to the graph
for parent, children in nodes.items():
    for child in children:
        G.add_edge(parent, child)

# Define node colors
colors = {
    "Queries in Microservices": "lightblue",
    "Read Queries": "lightgreen",
    "Write Queries": "lightcoral",
    "Transactional Queries": "lightgoldenrodyellow",
    "Caching Queries": "lightpink",
    "Search Queries": "lightseagreen"
}

# Assign colors to nodes
node_colors = []
for node in G.nodes:
    for key, color in colors.items():
        if node == key or node in nodes.get(key, []):
            node_colors.append(color)
            break
    else:
        node_colors.append("white")

# Draw the graph with a better layout
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G, seed=42)

nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, font_size=8, edge_color="gray", arrows=True, arrowstyle="->", arrowsize=10)
plt.title("Queries in Microservices Tree Structure")
plt.tight_layout()
plt.show()
