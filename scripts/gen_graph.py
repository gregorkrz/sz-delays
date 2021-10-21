import os
import json
from utils.load_stations import id_to_data

trains_path = "data/processed/trains.json"
edgelist_path = "data/processed/rail_network_edgelist.csv"
nodes_path = "data/processed/rail_network_nodes.csv"

trains = json.load(open(trains_path, "r"))

nodes = {}
edges = set()

for train_no in trains:
    data = trains[train_no]
    if data.get("train_type") == "LP" or data.get("train_type") == "LPV":
        # use local trains only - only those stop at all stations
        station_list =  data["train_stations"]
        for i in range(len(station_list) - 1):
            edge = (station_list[i]["id"], station_list[i+1]["id"])
            stredge = edge[0] + "," + edge[1]
            stredge_reversed = edge[1] + "," + edge[0]
            edges.add(stredge)
            edges.add(stredge_reversed)
            node_info = id_to_data[edge[0]]
            nodes[edge[0]] = [node_info["title"], node_info["lat"], node_info["lng"]]
            node_info = id_to_data[edge[1]]
            nodes[edge[1]] = [node_info["title"], node_info["lat"], node_info["lng"]]

out_edges = open(edgelist_path, "w")
out_nodes = open(nodes_path, "w")

out_nodes.write("id,station_name,lat,lng\n")
for edge in edges:
    out_edges.write(edge + "\n")
for stn in nodes:
    out_nodes.write("{},{},{},{}\n".format(stn, nodes[stn][0], nodes[stn][1], nodes[stn][2]))
out_edges.close()
