import pandas as pd
import matplotlib.pyplot as plt

nodes = "data/processed/rail_network_nodes.csv"

edgelist = "data/processed/rail_network_dropped.csv"

nodes = pd.read_csv(nodes)
edgelist = pd.read_csv(edgelist, header=None)

def get_coords(station_id):
    found_node = nodes[nodes["id"] == station_id].iloc[-1]
    return found_node["lat"], found_node["lng"]

fig, ax = plt.subplots()

for _, edge in edgelist.iterrows():
    y1, x1 = get_coords(edge[0])
    y2, x2 = get_coords(edge[1])
    plt.plot([x1, x2], [y1, y2], color="black", linewidth=0.1)

for _, node in nodes.iterrows():
    circle = plt.Circle((node["lng"], node["lat"]), radius=0.01)
    ax.add_patch(circle)
    label = ax.annotate(node["station_name"], xy=(node["lng"], node["lat"]), fontsize=5, ha="center")
ax.set_aspect('equal')