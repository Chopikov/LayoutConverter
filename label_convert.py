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
    src = './type1'
    dst = './dst'
    if not os.path.exists(src):
        print('Not such directory: ', src)
        exit(0)
    if not os.path.exists(dst):
        os.mkdir(dst)

    files = find_files(src)

    commons = ["wall_common_empty", "wall_common_filled",  "wall_common_cell", "wall_common_stroke",
               "wall_common_point", "wall_common_dotted-line"]

    bearings = ["wall_bearing_empty", "wall_bearing_filled", "wall_bearing_cell", "wall_bearing_stroke",
                "wall_bearing_point", "wall_bearing_dotted-line"]

    sinks = ["sink_common_bti", "sink_common_image_bti", "sink_common_type1", "sink_kitchen_bti",
             "sink_kitchen_image_bti",  "sink_kitchen_type1"]

    toilets = ["toilet_bti", "toilet_image_bti", "toilet_type1"]

    baths = ["bath_bti", "bath_image_bti",  "bath_type1"]

    stoves = ["stove_electric_bti",   "stove_electric_image_bti",  "stove_electric_type1",  "stove_gas_bti",
              "stove_gas_type1"]

    windows_balcony = ["window_balcony_bti", "window_balcony_type1"]

    risers = ["sewerage", "riser", "gutter_type2"]

    metas = ["_strange_", "trash-chute"]

    walls_balcony = ["wall_balcony_bti", "wall_balcony_type1"]

    # objs = ['window_common', 'wall_balcony', 'window_balcony', 'door_common', 'door_balcony', 'door_entrance',
    #         'sink_common', 'sink_kitchen', 'toilet', 'bath', 'stove_electric', 'stove_gas']

    for file in files:
        layout, name = load_json(file['path'])

        for shape in layout['shapes']:
            if shape['label'] == '__undefined__':
                print("Undefined in " + file['path'])

            if shape['label'] == 'door_entrance_bti':
                shape['label'] = 'door_common_bti'
            if shape['label'] == 'door_balcony_type1':
                shape['label'] = 'door_common_type1'
            if shape['label'] in metas:
                shape['label'] = 'meta'
            if shape['label'] in commons:
                shape['label'] = 'wall_common'
            if shape['label'] in bearings:
                shape['label'] = 'wall_bearing'
            if shape['label'] in windows_balcony:
                shape['label'] = 'window_balcony'
            if shape['label'] in walls_balcony:
                shape['label'] = 'wall_balcony'
            if shape['label'] in risers:
                shape['label'] = 'riser'
            if shape['label'] in sinks:
                shape['label'] = 'sink'
            if shape['label'] in toilets:
                shape['label'] = 'toilet'
            if shape['label'] in baths:
                shape['label'] = 'bath'
            if shape['label'] in stoves:
                shape['label'] = 'stove'

            # if shape['label'] == 'wall_thin':
            #     shape['label'] = 'wall_common'
            # if shape['label'] == 'door_thin':
            #     shape['label'] = 'door_common'
            # if shape['label'] == 'floor':
            #     shape['label'] = 'stair'
            # if shape['label'] in objs:
            #     shape['label'] = shape['label'] + '_bti'

            if not shape['label'] in config['LABEL_PRIORITY']:
                print(shape['label'], file['path'])

        with open(os.path.join(dst, name), 'w') as f:
            json.dump(layout, f, indent=2)

