import json


def write_json_to_file(data, file_path):
    with open(file_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False, default=str)


def read_json_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as outfile:
        data = json.load(outfile)
        return data
