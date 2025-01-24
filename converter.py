import csv
import json

DRIED_FRUITS_FILE = 'dried_fruits.csv'
NUTS_FILE = 'nuts.csv'
OTHER_FILE = 'other.csv'

def load_file_json(name):
    try:
        with open(name, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError):
        return {}

def load_file_csv(name):
    try:
        with open(name, "r", encoding="utf-8") as file:
            return list(csv.reader(file))
    except (FileNotFoundError):
        return {}

def save_in_json(name, data):
    with open(name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(load_file_json(name))

def converter(csv_file):
    csv_data = load_file_csv(csv_file)
    name_json = csv_file.replace(".csv", ".json")
    new_data = dict()
    for row in csv_data:
        new_data[row[0]] = [row[1], row[2]]
    save_in_json(name_json, new_data)

converter(OTHER_FILE)

# print(type(load_file(DRIED_FRUITS_FILE)))
# print(load_file(DRIED_FRUITS_FILE))
