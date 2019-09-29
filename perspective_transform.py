import cv2
import os
import math
import numpy as np
import json
import base64
import os

from utils import find_files, load_json


src_images = './images'
src_photos = './photos'
src_layout = './layouts'
dst_layout = './new_layouts'


files = find_files(src_images, '.png')
photos = find_files(src_photos, '.jpg')
for file in files:
    file_name = os.path.split(file['path'])[1]
    file_name_without = os.path.splitext(file_name)[0]

    file_img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    height = file_img.shape[0]
    width = file_img.shape[1]

    for photo in photos:
        photo_name = os.path.split(file['path'])[1]
        photo_name_without = os.path.splitext(file_name)[0]
        if photo_name_without.find(file_name_without) == -1:
            continue

        img = cv2.imread(photo_name, cv2.IMREAD_GRAYSCALE)

        black = np.full_like(img, np.uint8(255))
        black[img < 40] = 0
        black = cv2.bitwise_not(black)

        black = cv2.dilate(black, np.ones((5, 5), np.uint8), iterations=1)
        black = cv2.erode(black, np.ones((5, 5), np.uint8), iterations=1)

        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(black, 8, cv2.CV_32S)

        l_u = [10000, 10000]
        dist_l_u = 10000
        count_l_u = -1
        r_u = [10000, 10000]
        dist_r_u = 10000
        count_r_u = -1
        r_d = [10000, 10000]
        dist_r_d = 10000
        count_r_d = -1
        l_d = [10000, 10000]
        dist_l_d = 10000
        count_l_d = -1

        for i in range(nb_components):

            dist = math.hypot(centroids[i][0] - 0, centroids[i][1] - 0)
            if dist < dist_l_u:
                l_u = centroids[i]
                dist_l_u = dist
                count_l_u = i

            dist = math.hypot(img.shape[1] - centroids[i][0], centroids[i][1] - 0)
            if dist < dist_r_u:
                r_u = centroids[i]
                dist_r_u = dist
                count_r_u = i

            dist = math.hypot(img.shape[1] - centroids[i][0], img.shape[0] - centroids[i][1])
            if dist < dist_r_d:
                r_d = centroids[i]
                dist_r_d = dist
                count_r_d = i

            dist = math.hypot(centroids[i][0] - 0, img.shape[0] - centroids[i][1])
            if dist < dist_l_d:
                l_d = centroids[i]
                dist_l_d = dist
                count_l_d = i

        # new_img = np.zeros_like(output, np.uint8)
        # new_img[output == count_l_u] = 255
        # cnt = cv2.findContours(new_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # new_img.fill(0)
        # cv2.drawContours(new_img, cnt[0], 0, 128, 3)

        # cv2.circle(black, tuple(l_u.astype(int)), 5, 128, -1)
        # cv2.circle(black, tuple(r_u.astype(int)), 5, 128, -1)
        # cv2.circle(black, tuple(r_d.astype(int)), 5, 128, -1)
        # cv2.circle(black, tuple(l_d.astype(int)), 5, 128, -1)
        #
        # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('img', img.shape[1] // 3, img.shape[0] // 3)
        # cv2.imshow('img', black)
        # cv2.waitKey(0)

        initial_width = 595
        # initial_height = 842
        half_square_size = 25

        real_width = int(math.hypot(r_d[0] - l_u[0], r_d[1] - l_u[1]))
        half_square_size *= (real_width / initial_width)
        M = cv2.getPerspectiveTransform(np.array([l_u, r_u, r_d, l_d], np.float32),
                                        np.array([[half_square_size, half_square_size],
                                                  [real_width - half_square_size, half_square_size],
                                                  [real_width - half_square_size, real_width - half_square_size],
                                                  [half_square_size, real_width - half_square_size]], np.float32))

        M_inverse = np.linalg.inv(M)

        layout = load_json(os.path.join(src_layout, file_name_without + '.json'))

        h = real_width
        w = int(h * width / height)
        if w > real_width:
            w = real_width
            h = int(height / width * w)
        # sy = int((initial_height - h) / 2)
        sy = int((real_width - h) / 2)
        sx = int((real_width - w) / 2)

        for shape in layout['shapes']:
            points = shape['points']
            for i, _ in enumerate(points):
                points[i] = (sx + _[0]*w/width, sy + _[1]*h/height)

        for shape in layout['shapes']:
            points = shape['points']
            for i, _ in enumerate(points):
                vector = [_[0], _[1], 1.0]
                new_vector = M_inverse.dot(vector)
                new_vector /= new_vector[2]
                points[i] = (new_vector[0], new_vector[1])

        with open(file_name, "rb") as image_file:
            layout['imageData'] = base64.b64encode(image_file.read()).decode('utf-8')
            layout['imagePath'] = file_name

        with open(os.path.join(dst_layout, file_name_without + '.json'), 'w') as f:
            json.dump(layout, f, indent=2)

        # cv2.namedWindow('orig', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('orig', img.shape[1] // 3, img.shape[0] // 3)
        # warped = cv2.warpPerspective(img, M, (real_width, real_width))
        # orig = cv2.warpPerspective(warped, M_inverse, (img.shape[1], img.shape[0]))
        # cv2.imshow('warped', warped)
        # cv2.imshow('orig', orig)
        # cv2.waitKey(0)
