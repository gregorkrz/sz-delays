import json

stations_path = "data/raw/stations.json"

stations = json.load(open(stations_path, "r"))

name_to_id = {}
id_to_data = {}

def try_float(number):
    try:
        return float(number)
    except:
        return None

def get_coords(name, lat, lng):
    if not (try_float(lat) and try_float(lng)):
        if name.startswith("Trst"):
            return 45.6577528, 13.7719334
        elif name.startswith("Opčine"):
            return 45.6941713, 13.7913032
        elif name.startswith("Divača(Škocjanske jame)"):
            return 45.675113, 14.019581
        else:
            return None, None
    else:
        return float(lat), float(lng)

for station in stations:
    num, title, lat, lng = station["st"], station["naziv"], station["Geo_sirina"], station["Geo_dolzina"]
    t = title.strip()
    if t in name_to_id:
        raise Exception("Error! Title", t, "already in stations")
    name_to_id[t] = num
    lat, lng = get_coords(title, lat, lng)
    id_to_data[num] = {"title": title, "lat": lat, "lng": lng}

