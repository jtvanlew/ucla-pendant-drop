import cv2
from numpy import *
from matplotlib     import pyplot as plt, cm, colors
from scipy      	import optimize
import sys

BLACK = (0, 0, 0)
imageFile = sys.argv[1]
img = cv2.imread(imageFile)

# get height and width of droplet, then get centroid
# if the image has been centered between the ritcle, the
# centroid ought to be half the width and height
h, w = img.shape[0:2]
c1, c2 = w/2, h/2

# draw a large black circle in the center of the image to
# block out any reflections in the droplet
cv2.circle(img, (c1, c2), w/6, BLACK, thickness=-1)
cv2.imwrite('output/droplet_filled.jpg', img)

threshold_low  = 20
threshold_high = 225

# pull out edges of the entire droplet
ret,dropletFull = cv2.threshold(img,threshold_low,threshold_high,cv2.THRESH_BINARY)
fullEdges = cv2.Canny(dropletFull, 30, 80)
dropletFull[fullEdges != 0] = (0, 255, 0)
cv2.imwrite('output/droplet_filled_threshold_'+str(threshold_low)+'.jpg', dropletFull)
cv2.imwrite('output/droplet_filled_edges_'+str(threshold_low)+'.jpg', fullEdges)



# Pull out just the bottom of the droplet in order to find the radius of curvature
r1 = 300
x1, x2 = c1-r1, c1+r1
y1, y2 = c2, c2+r1
dropletBottom = img[y1:y2, x1:x2]       
ret,dropletBottom = cv2.threshold(dropletBottom,threshold_low,threshold_high,cv2.THRESH_BINARY)
edges = cv2.Canny(dropletBottom, 30, 80)
dropletBottom[edges != 0] = (0, 255, 0)

cv2.imwrite('output/droplet_bottom_filled.jpg_'+str(threshold_low)+'.jpg', dropletBottom)
cv2.imwrite('output/droplet_bottom_filled_edges_'+str(threshold_low)+'.jpg',edges)
# save('output/edges',edges)
# ========================================================





















