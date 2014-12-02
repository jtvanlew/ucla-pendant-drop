import cv2
import numpy as np
from matplotlib     import pyplot as plt, cm, colors
from scipy      	import optimize


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






# do least squares with jacobian to find radius
count1 = 0
x = []
y = []

# move through the rows and columns of image matrix and 
# pull out the x and y coordinates of the data
for row in matrix:
    count2 = len(matrix)
    for column in row:
        w = linalg.norm(column)
        if w > 0:
            x.append(count1)
            y.append(count2)
        count2 -= 1
    count1 += 1

x = array(x)
y = array(y)

# Coordinates of the 2D points
R = arange(0, 2*pi, 0.5)
basename = 'circle'


# coordinates of the barycenter
x_m = mean(x)
y_m = mean(y)
method_2b  = "leastsq with jacobian"

def calc_R(xc, yc):
    """ calculate the distance of each 2D points from the center c=(xc, yc) """
    return sqrt((x-xc)**2 + (y-yc)**2)

def f_2b(c):
    """ calculate the algebraic distance between the 2D points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(*c)
    return Ri - Ri.mean()

def Df_2b(c):
    """ Jacobian of f_2b
    The axis corresponding to derivatives must be coherent with the col_deriv option of leastsq"""
    xc, yc     = c
    df2b_dc    = empty((len(c), x.size))

    Ri = calc_R(xc, yc)
    df2b_dc[ 0] = (xc - x)/Ri                   # dR/dxc
    df2b_dc[ 1] = (yc - y)/Ri                   # dR/dyc
    df2b_dc       = df2b_dc - df2b_dc.mean(axis=1)[:, newaxis]

    return df2b_dc

center_estimate = x_m, y_m
center_2b, ier = optimize.leastsq(f_2b, center_estimate, Dfun=Df_2b, col_deriv=True)

xc_2b, yc_2b = center_2b
Ri_2b        = calc_R(xc_2b, yc_2b)
R_2b         = Ri_2b.mean()