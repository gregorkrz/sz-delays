# Create delay CSV

import os
import json
from utils.load_stations import id_to_data, name_to_id
import pandas as pd
import numpy as np


input_delays_path = "data/processed/cleaned.json"
output_path = "data/processed/delays.csv"
trains_path = "data/processed/trains.json"

out = open(output_path, "w")
out.write("timestamp,train_no,train_type,station_id,delay_type,delay\n")
delays = json.load(open(input_delays_path, "r"))
trains = json.load(open(trains_path, "r"))

for object in delays:
    #print(object)
    ts = object["_id"]
    for delay in object["delays"]:
        trainnumber = delay["trainnumber"]
        if trainnumber in trains:
            traintype = trains[trainnumber]["train_type"]
        elif trainnumber == "502":
            traintype = "IC"
        stn = name_to_id.get(delay["station"])
        tod = delay["typeofdelay"]
        if tod == 68:
            tod = "D"
        elif tod == 69:
            tod = "E"
        elif tod == 65:
            tod = "A"
        else:
            raise Exception("TOD not known")

        if not stn:
            print("Station", delay["station"], "not found")
        else:
            out.write("{},{},{},{},{},{}\n".format(ts, trainnumber, traintype, stn, tod, delay["delay"]))

out.close()