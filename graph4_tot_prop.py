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
        G.add_edge(parent, child, label=f"{prob:.1f}", weight=prob)

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

# Calculate cumulative probabilities for leaf nodes
cumulative_probs = {}
for parent, services in leaf_nodes.items():
    for service in services:
        paths = list(nx.all_simple_paths(G, source="Queries", target=parent))
        cumulative_prob = 0
        for path in paths:
            prob = 1
            for i in range(len(path) - 1):
                prob *= G[path[i]][path[i+1]]['weight']
            cumulative_prob += prob
        cumulative_probs[service] = cumulative_prob

# Add leaf nodes to the graph and change their color/shape
for parent, services in leaf_nodes.items():
    for service in services:
        G.add_edge(parent, service)
        G.nodes[service]['color'] = 'red'
        G.nodes[service]['shape'] = 'box'
        G.nodes[service]['label'] = f"{service}\n{cumulative_probs[service]:.2f}"
        print(G.nodes[service]['label'])

# Set color based on cumulative probability
def get_color(prob):
    if prob >= 0.05:
        return 'red'
    elif prob >= 0.03:
        return 'orange'
    else:
        return 'yellow'

for service in cumulative_probs:
    G.nodes[service]['fillcolor'] = get_color(cumulative_probs[service])

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

# Set leaf node colors and labels
for service, prob in cumulative_probs.items():
    node = G_pg.get_node(service)
    node.attr['label'] = f"{service}\n{prob:.1f}"
    node.attr['fillcolor'] = get_color(prob)

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
    mpatches.Patch(color='lightseagreen', label='Queries', edgecolor='black'),
    mpatches.Patch(color='green', label='Read/Write Queries', edgecolor='black'),
    mpatches.Patch(color='lightgreen', label='Sub Queries', edgecolor='black'),
    mpatches.Patch(color='white', label='Leaf Nodes', edgecolor='black'),
    mpatches.Patch(color='red', label='Microservices (high prob)', edgecolor='black'),
    mpatches.Patch(color='orange', label='Microservices (medium prob)', edgecolor='black'),
    mpatches.Patch(color='yellow', label='Microservices (low prob)', edgecolor='black')
]

# Add legend to the graph
plt.legend(handles=legend_elements, loc='upper left', fontsize=14)

# Show the final plot with the legend
plt.savefig("graph.png")
