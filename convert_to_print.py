import cv2
import numpy as np
import os

from utils import find_files

src = './images'
dst = './images_print'

files = find_files(src, '.png')
for file in files:
    file_name = os.path.split(file['path'])[1]
    file_name_without = os.path.splitext(file_name)[0]

    img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    old_w = img.shape[1]
    old_h = img.shape[0]
    new_w = 595
    new_h = 842
    square_size = 50
    min_dim = min(new_h, new_w)

    shift_up = int((new_h - min_dim) / 2)
    shift_down = (new_h - min_dim) - shift_up

    new_img = cv2.resize(img, (min_dim, min_dim))

    s = np.full((new_h, new_w), np.uint8(255))
    sy = int((new_h - min_dim) / 2)
    sx = int((new_w - min_dim) / 2)
    s[sy:sy + min_dim, sx:sx + min_dim] = new_img
    s[shift_up:square_size + shift_up, 0:square_size] = 0
    s[shift_up:square_size + shift_up, s.shape[1] - square_size:s.shape[1]] = 0
    s[s.shape[0] - square_size - shift_down:s.shape[0] - shift_down, 0:square_size] = 0
    s[s.shape[0] - square_size - shift_down:s.shape[0] - shift_down, s.shape[1] - square_size:s.shape[1]] = 0

    cv2.imwrite(os.path.join(dst, file_name), s)


# cv2.imwrite('./res.png', s)
# cv2.imshow('img', s)
# cv2.waitKey(0)

