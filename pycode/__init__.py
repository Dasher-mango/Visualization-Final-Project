# import csv
# import os
# import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Sample data representing connections between nodes
edges = [
    ('A', 'B'),
    ('B', 'C'),
    ('D', 'E'),
    ('E', 'F'),
    ('G', 'H'),
    ('H', 'I'),
    ('I', 'G'),
]

# Create a graph from the edges
G = nx.Graph()
G.add_edges_from(edges)

# Find connected components
connected_components = list(nx.connected_components(G))

# Print the connected components
print("Connected Components:", connected_components)

# Visualize the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=1000, font_size=10)
plt.show()
