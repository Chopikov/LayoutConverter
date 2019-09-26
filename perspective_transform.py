import cv2
import math
import numpy as np

img = cv2.imread('./img.jpg', cv2.IMREAD_GRAYSCALE)

black = np.full_like(img, np.uint8(255))
black[img < 40] = 0
black = cv2.bitwise_not(black)

black = cv2.dilate(black, np.ones((5, 5), np.uint8), iterations=1)
black = cv2.erode(black, np.ones((5, 5), np.uint8), iterations=1)

nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(black, 8, cv2.CV_32S)
# cnts, hier = cv2.findContours(black, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

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

# black.fill(0)
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

cv2.circle(black, tuple(l_u.astype(int)), 5, 128, -1)
cv2.circle(black, tuple(r_u.astype(int)), 5, 128, -1)
cv2.circle(black, tuple(r_d.astype(int)), 5, 128, -1)
cv2.circle(black, tuple(l_d.astype(int)), 5, 128, -1)

# cv2.namedWindow('img', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('img', img.shape[1] // 3, img.shape[0] // 3)
# cv2.imshow('img', black)
# cv2.waitKey(0)

M = cv2.getPerspectiveTransform(np.array([l_u, r_u, r_d, l_d], np.float32), np.array([[0, 0], [595, 0], [595, 842], [0, 842]], np.float32))

warped = cv2.warpPerspective(img, M, (512, 512))
cv2.imshow('warped', warped)
cv2.waitKey(0)
print(M)
