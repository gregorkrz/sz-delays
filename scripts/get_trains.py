import os

filepath = "data/processed/existing_train_numbers.csv"

data = open(filepath, "r").read().split("\n")[:-1]

for train in data:
    stream = os.popen("node scripts/node/get_train.js " + train)
    output  = stream.read()
    print(output)
