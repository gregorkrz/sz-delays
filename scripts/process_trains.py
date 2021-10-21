import json
import os
from utils.load_stations import id_to_data, name_to_id


trains_dir = "data/raw/trains"
processed_trains_path = "data/processed/trains.json"


def getMultiple(dictionary, *args):
    return [dictionary.get(x) for x in args]

trains = {}

for train_json in os.listdir(trains_dir):
    train_path = os.path.join(trains_dir, train_json)
    train_data = json.load(open(train_path, "r"))
    train_no, train_type, train_stations = getMultiple(train_data, "st_vlaka", "Vrsta", "Postaja")
    if train_no is None or train_type is None or train_stations is None:
        #print("invalid API response:", train_data)
        continue
    if train_no in trains:
        raise Exception("train", train_no, "already exists")
    stations_ids = []
    for station in train_stations:
        title, arr, dep = getMultiple(station, "Naziv", "Prihod", "Odhod")
        if title not in name_to_id:
            print("WARNING: station", title, "not in station index - will be dropped from the timetable for now")
        else:
            stn_id = name_to_id[title]
            stations_ids.append({"id": stn_id, "arr": arr, "dep": dep})
    trains[train_no] = {"train_type": train_type, "train_stations": stations_ids}

out = open(processed_trains_path, "w")
out.write(json.dumps(trains))
out.close()