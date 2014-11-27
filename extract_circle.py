import cv2
import numpy as np
from matplotlib import pyplot as plt


BLACK = (0, 0, 0)

img = cv2.imread('droplets/droplet_shifted.jpg')

h, w = img.shape[0:2]

c1, c2 = w/2, h/2

cv2.circle(img, (c1, c2), w/8, BLACK, thickness=-1)
r1 = 125
x1, x2 = c1-r1, c1+r1
y1, y2 = c2-50, c2+140

img = img[y1:y2, x1:x2]       
ret,img = cv2.threshold(img,20,225,cv2.THRESH_BINARY)
edges = cv2.Canny(img, 30, 80)
img[edges != 0] = (0, 255, 0)

#plt.imshow(img)
cv2.imwrite('output/droplet_filled.jpg', img)
cv2.imwrite('output/droplet_edges.jpg',edges)
np.save('output/edges',edges)