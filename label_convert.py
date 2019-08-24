import json
import os


def find_files(folder):
    if folder is None:
        raise Exception('Finding of files failed')

    try:
        tree = os.walk(folder)
        files = []
        for _ in tree:
            files = files.__add__([{'path': os.path.join(_[0], f), 'name': f}
                                   for f in filter(lambda x: x[-5:].lower() == '.json', _[2])])
    except WindowsError:
        raise Exception('Finding of files failed')
    return files


def load_json(cfg_path):
    with open(cfg_path, 'r') as f:
        cfg = json.load(f)
    file_name = os.path.split(cfg_path)[1]
    return cfg, file_name


if __name__ == "__main__":
    config, config_name = load_json('./config.json')
    src = './new'
    dst = './dst'
    if not os.path.exists(src):
        print('Not such directory: ', src)
        exit(0)
    if not os.path.exists(dst):
        os.mkdir(dst)

    files = find_files(src)

    objs = ['window_common', 'wall_balcony', 'window_balcony', 'door_common', 'door_balcony', 'door_entrance',
            'sink_common', 'sink_kitchen', 'toilet', 'bath', 'stove_electric', 'stove_gas']

    for file in files:
        layout, name = load_json(file['path'])

        for shape in layout['shapes']:
            if shape['label'] == '__undefined__':
                print("Undefined in " + file['path'])

            if shape['label'] == 'door_entrance':
                shape['label'] = 'door_common'
            if shape['label'] == 'wall_common':
                shape['label'] = 'wall_common_empty'
            if shape['label'] == 'floor':
                shape['label'] = 'stair'
            if shape['label'] in objs:
                shape['label'] = shape['label'] + '_type1'

            if not shape['label'] in config['LABEL_PRIORITY']:
                print(shape['label'], file['path'])

        with open(os.path.join(dst, name), 'w') as f:
            json.dump(layout, f, indent=2)

