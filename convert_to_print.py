import cv2
import numpy as np

img = cv2.imread('./test.png', cv2.IMREAD_GRAYSCALE)
old_w = 512
old_h = 512
new_w = 595
new_h = 842
square_size = 50
s = np.full((new_h, new_w), np.uint8(255))
sy = int((new_h - old_h) / 2)
sx = int((new_w - old_w) / 2)
s[sy:sy + old_h, sx:sx + old_w] = img
s[0:square_size, 0:square_size] = 0
s[0:square_size, s.shape[1] - square_size:s.shape[1]] = 0
s[s.shape[0] - square_size:s.shape[0], 0:square_size] = 0
s[s.shape[0] - square_size:s.shape[0], s.shape[1] - square_size:s.shape[1]] = 0

cv2.imwrite('./res.png', s)
cv2.imshow('img', s)
cv2.waitKey(0)

