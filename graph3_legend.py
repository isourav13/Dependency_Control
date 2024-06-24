import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv
import matplotlib.patches as mpatches

# Create a directed graph
G = nx.DiGraph()

# Define nodes and their hierarchical relationships with probabilities
nodes = {
    "Queries": {"Read Queries": 0.7, "Write Queries": 0.3},
    "Read Queries": {"Simple Reads": 0.3, "Complex Reads": 0.4, "Filtered Reads": 0.2, "Aggregations": 0.1},
    "Filtered Reads": {"Range Queries": 0.5, "Multi-attribute Filters": 0.5},
    "Aggregations": {"Count": 0.4, "Sum": 0.3, "Min/Max": 0.3},
    "Complex Reads": {"Inner Joins": 0.6, "Left Joins": 0.1, "Right Joins": 0.1, "Full Joins": 0.2},
    "Write Queries": {"Create": 0.4, "Update": 0.3, "Delete": 0.2, "Upsert": 0.1},
    "Create": {"Single Create": 0.6, "Bulk Create": 0.4},
    "Update": {"Full Update": 0.4, "Partial Update (Patch)": 0.4, "Bulk Update": 0.2},
    "Delete": {"Soft Delete": 0.5, "Hard Delete": 0.5}
}

# Define node colors
colors = {
    "Queries": "lightseagreen",
    "Read Queries": "green",
    "Write Queries": "green",
    "Simple Reads": "lightgreen",
    "Complex Reads": "lightgreen",
    "Filtered Reads": "lightgreen",
    "Aggregations": "lightgreen",
    "Create": "lightgreen",
    "Update": "lightgreen",
    "Upsert": "lightgreen",
    "Delete": "lightgreen"
}

# Add edges with probabilities to the graph
for parent, children in nodes.items():
    for child, prob in children.items():
        G.add_edge(parent, child, label=f"{prob:.1f}")

# Add microservices as leaf nodes
leaf_nodes = {
    "Simple Reads": ["Catalog Service", "Authentication Service", "Payment Service"],
    "Range Queries": ["Search Service"],
    "Multi-attribute Filters": ["Search Service"],
    "Count": ["Cart Service", "Notification Service"],
    "Sum": ["Cart Service"],
    "Min/Max": ["Catalog Service"],
    "Inner Joins": ["Order History Service", "Support History Service"],
    "Left Joins": ["Customer Information Service", "Product Review Service"],
    "Right Joins": ["Vendor Service"],
    "Full Joins": ["Customer Information Service"],
    "Single Create": ["Customer Information Service", "Catalog Upload Service"],
    "Bulk Create": ["Bulk Catalog Upload Service", "Order Service"],
    "Full Update": ["Catalog Service", "Customer Information Service"],
    "Partial Update (Patch)": ["Customer Preferences Service", "Order Service"],
    "Bulk Update": ["Inventory Update Service"],
    "Soft Delete": ["Cart Service", "Wishlist Service"],
    "Hard Delete": ["Order History Service"],
    "Upsert": ["Inventory Update Service", "Catalog Service"]
}

# Add leaf nodes to the graph and change their color/shape
for parent, services in leaf_nodes.items():
    for service in services:
        G.add_edge(parent, service)
        G.nodes[service]['color'] = 'red'
        G.nodes[service]['shape'] = 'box'

# Create a pygraphviz AGraph from the NetworkX graph for better layout
G_pg = nx.nx_agraph.to_agraph(G)
G_pg.graph_attr.update(rankdir="LR")  # Set the layout direction to left-to-right
G_pg.node_attr.update(style="filled", fontsize=20)  # Increase font size for nodes
G_pg.edge_attr.update(fontsize=16)  # Increase font size for edge labels

# Set node colors
for node in G_pg.nodes():
    if node in colors:
        node.attr['fillcolor'] = colors[node]
    else:
        node.attr['fillcolor'] = "white"

# Draw the graph
plt.figure(figsize=(30, 20))  # Adjust figsize to accommodate left-to-right layout
G_pg.layout(prog="dot")  # Use 'dot' layout algorithm for hierarchical graphs
G_pg.draw(path="graph.png", format="png")

# Load the drawn graph
img = plt.imread("graph.png")
plt.figure(figsize=(30, 20))
plt.imshow(img)
plt.axis('off')

# Create the legend
legend_elements = [
    mpatches.Patch(color='lightseagreen', label='Queries'),
    mpatches.Patch(color='green', label='Read/Write Queries'),
    mpatches.Patch(color='lightgreen', label='Leaf Nodes'),
    mpatches.Patch(color='white', label='Leaf Nodes'),
    mpatches.Patch(color='red', label='Microservices')
]

# Add legend to the graph
plt.legend(handles=legend_elements, loc='upper left', fontsize=14)

# Show the final plot with the legend
plt.savefig("graph.png")
