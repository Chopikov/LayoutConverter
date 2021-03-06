import os
import sys
import base64
import cv2
import numpy as np

from utils import find_files, load_json


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
    cv2.fillPoly(dst, [np.asarray(points)], color)


def contrast(src, contrast_shift):
    adjust = (contrast_shift + 100.0) / 100.0
    adjust = adjust * adjust
    dst = src.copy().astype(np.float32)
    dst = np.clip((((dst / 255.0 - 0.5) * adjust + 0.5) * 255.0), 0, 255)
    return dst.astype(np.uint8)


if __name__ == "__main__":

    config = load_json('./config.json')

    DRAW_MAP = {
        'rectangle': draw_rect,
        'polygon': draw_polygon,
    }
    COLOR_MAP = config['COLOR_MAP_BINARY']

    src = './res'
    dst_img = './image1'
    dst_mask = './mask1'

    if len(sys.argv) > 1:
        src = sys.argv[1]
    if not os.path.exists(src):
        print('Not such directory: ', src)
        exit(0)
    if not os.path.exists(dst_img):
        os.mkdir(dst_img)
    if not os.path.exists(dst_mask):
        os.mkdir(dst_mask)

    files = find_files(src, '.json')

    for file in files:
        layout = load_json(file['path'])
        img_bytes = base64.b64decode(layout['imageData'])
        img_curr = cv2.imdecode(np.fromstring(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        img_resized = convert_image(img_curr, layout)
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

        shape = img_gray.shape
        img_mask = np.full((shape[0], shape[1]), np.uint8(0))

        for label in config['LABEL_PRIORITY']:
            objs = filter(lambda x: x['label'] == label, layout['shapes'])
            for o in objs:
                DRAW_MAP[o['shape_type']](img_mask, COLOR_MAP[label], o['points'])
        file_name = os.path.splitext(file['name'])[0]

        cv2.imwrite(os.path.join(dst_img, file_name) + '.png', img_gray)
        cv2.imwrite(os.path.join(dst_mask, file_name) + '.png', img_mask)
        print(file_name)
