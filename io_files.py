import json

def save_dict_in_file(dict, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dict, f, ensure_ascii=False)

def load_dict_in_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        dict = json.load(f)
    return dict
