import json


def read(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def write(file_path, content):
    with open(file_path, 'w') as json_file:
        json.dump(content, json_file)
