# This script drops manually selected edges. For now it will be OK solution.

import os
import json
from utils.load_stations import id_to_data, name_to_id
import pandas as pd
import numpy as np

edgelist_path = "data/processed/rail_network_edgelist.csv"
max_shortcut_len = 5
output_edgelist_path = "data/processed/rail_network_dropped.csv"

edges_to_drop = ["Hrastovlje,Hrpelje-Kozina", "Divača,Sežana", "Divača,Pivka", "Pivka,Gornje Ležeče", 
"Postojna,Pivka", "Velika Loka,Trebnje", "Mirna Peč,Novo mesto Center", "Trebnje,Mirna", "Trebnje,Gomila",
"Velika Nedelja,Ptuj", "Ptuj,Kidričevo", "Hoče,Maribor", "Maribor,Maribor Studenci", "Ruše,Ruta", "Ruta,Podvelka",
"Podvelka,Vuhred", "Vuhred,Vuzenica", "Vuzenica,Dravograd", "Borovnica,Ljubljana Tivoli", "Medvode,Ljubljana Vižmarje",
"Plave,Nova Gorica", "Volčja Draga,Prvačina", "Škofljica,Grosuplje", "Grosuplje,Žalna", "Višnja Gora,Ivančna Gorica", "Ivančna Gorica,Radohova vas", "Mirna Peč,Novo mesto",
"Maribor Studenci,Ruše", "Logatec,Rakek"]

edgelist_to_drop = []

for i in range(len(edges_to_drop)):
    print(edges_to_drop[i])
    a, b = edges_to_drop[i].split(",")
    a, b = int(name_to_id[a]), int(name_to_id[b])
    edgelist_to_drop.append([a, b]) 
    edgelist_to_drop.append([b, a]) 


edgelist = pd.read_csv(edgelist_path, header=None).values.tolist()

new_edgelist = []

for edge in edgelist:
    if edge not in edgelist_to_drop:
        new_edgelist.append(edge)

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