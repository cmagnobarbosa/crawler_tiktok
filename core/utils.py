"""Utils module"""
import json


def write_json(data, filename='data.json'):
    """Write data to a json file"""
    with open(filename, 'w', encoding='utf8') as arq:
        json.dump(data, arq, indent=4, ensure_ascii=False)
