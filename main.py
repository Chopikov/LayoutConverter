import os
import sys
import json
import base64
import cv2
import numpy as np


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
    # config_path = os.path.split(cfg_path)[0]
    return cfg


def convert_image(img, layout):
    if img is None:
        return
    height, width, channels = img.shape
    rect = (0, 0, 512, 512)
    h = rect[3]
    w = int(h * width / height)
    if w > rect[2]:
        w = rect[2]
        h = int(height / width * w)
    new_img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    s = np.full((rect[3], rect[2], 3), np.uint8(255))
    sy = int((rect[3] - h) / 2)
    sx = int((rect[2] - w) / 2)
    s[sy:sy + h, sx:sx + w] = new_img

    for shape in layout['shapes']:
        points = shape['points']
        for i, _ in enumerate(points):
            points[i] = (int(sx + _[0]*w/width), int(sy + _[1]*h/height))
    return s


def draw_rect(dst, color, points):
    cv2.rectangle(dst, points[0], points[1], color, thickness=-1)


def draw_polygon(dst, color, points):
    cv2.fillConvexPoly(dst, np.asarray(points), color)


if __name__ == "__main__":

    config = load_json('./config.json')

    DRAW_MAP = {
        'rectangle': draw_rect,
        'polygon': draw_polygon,
    }
    COLOR_MAP = config['COLOR_MAP']

    src = './src'
    dst_img = './img'
    dst_mask = './mask'
    if len(sys.argv) > 1:
        src = sys.argv[1]
    if not os.path.exists(src):
        print('Not such directory: ', src)
        exit(0)
    if not os.path.exists(dst_img):
        os.mkdir(dst_img)
    if not os.path.exists(dst_mask):
        os.mkdir(dst_mask)
    files = find_files(src)

    for file in files:
        layout = load_json(file['path'])
        img_bytes = base64.b64decode(layout['imageData'])
        img_curr = cv2.imdecode(np.fromstring(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        img_resized = convert_image(img_curr, layout)
        shape = img_resized.shape
        img_mask = np.full((shape[0], shape[1]), np.uint8(255))

        for label in config['LABEL_PRIORITY']:
            objs = filter(lambda x: x['label'] == label, layout['shapes'])
            for o in objs:
                DRAW_MAP[o['shape_type']](img_mask, COLOR_MAP[label], o['points'])
        file_name = os.path.splitext(file['name'])[0]

        cv2.imwrite(os.path.join(dst_img, file_name) + '.png', img_resized)
        cv2.imwrite(os.path.join(dst_mask, file_name) + '.png', img_mask)
        print(file_name)
