# WIP. This does not arrive at correct solution for now



import os
import json
from utils.load_stations import id_to_data, name_to_id
import pandas as pd
import numpy as np

edgelist_path = "data/processed/rail_network_edgelist.csv"
max_shortcut_len = 5
output_edgelist_path = "data/processed/rail_network_5.csv"
# drop edge if alternative path from i-->j exists with length <= 5

def create_edgelist_dict(edgelist):
    g = {}
    for edge in edgelist:
        s, e = edge[0], edge[1]
        if s not in g:
            g[s] = set()
        if e not in g:
            g[e] = set()
        g[s].add(e)
        g[e].add(s)
    return g

edgelist = pd.read_csv(edgelist_path, header=None).values
G = create_edgelist_dict(edgelist)

def find_path(i, j, blacklist=[], max_len=max_shortcut_len):
    if i == j:
        return True
    if max_len == 0:
        return False
    for neighbor in G[i]:
        if set([neighbor, i]) in blacklist:
            continue
        if find_path(neighbor, j, blacklist + [set([i, neighbor])], max_len=max_len-1):
            return True
    return False

new_edgelist = []

for edge in edgelist:
    i, j = edge[0], edge[1]
    path = find_path(i, j, blacklist=[set([i, j])])
    if not path:
        # the edge is really needed 
        new_edgelist.append(list(edge))

def is_undirected(edgelist):
    # very slow but written in 30 secs  ¯\_(ツ)_/¯
    for edge in edgelist:
        if [edge[1], edge[0]] not in edgelist:
            return False
    return True

def is_unique(edgelist):
    # very slow but written in 30 secs  ¯\_(ツ)_/¯
    for i in range(len(edgelist)):
        if edgelist[i] in edgelist[:i] + edgelist[i+1:]:
            return False
    return True

print(is_undirected(new_edgelist), is_unique(new_edgelist))

#new_edgelist = np.array(new_edgelist)

f = open(output_edgelist_path, "w")
for edge in new_edgelist:
    f.write("{},{}\n".format(edge[0], edge[1]))

f.close()