import osmnx as ox
import networkx as nx
import math
import matplotlib.pyplot as plt


place = "National Chiao Tung University, Hsinchu"
# Download the street network graph for the area
G = ox.graph_from_place(place, network_type="walk")

fig, ax = ox.plot_graph(G, node_size=0)
fig.savefig("route_plot.png", dpi=300, bbox_inches='tight')
# Get edge geometries for the route
nodes, edges = ox.graph_to_gdfs(G)
plt.close(fig) 