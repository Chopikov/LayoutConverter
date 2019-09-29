import os
import json


def find_files(folder, extension):
    if folder is None:
        raise Exception('Finding of files failed')

    try:
        tree = os.walk(folder)
        files = []
        for _ in tree:
            files = files.__add__([{'path': os.path.join(_[0], f), 'name': f}
                                   for f in filter(lambda x: x[-len(extension):].lower() == extension, _[2])])
    except WindowsError:
        raise Exception('Finding of files failed')
    return files


def load_json(cfg_path):
    with open(cfg_path, 'r') as f:
        cfg = json.load(f)
    # config_path = os.path.split(cfg_path)[0]
    return cfg
