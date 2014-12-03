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


# pull out edges of the entire droplet
ret,dropletFull = cv2.threshold(img,20,225,cv2.THRESH_BINARY)
fullEdges = cv2.Canny(dropletFull, 30, 80)
dropletFull[fullEdges != 0] = (0, 255, 0)
#plt.imshow(dropletFull)



# Pull out just the bottom of the droplet in order to find the radius of curvature
r1 = 300
x1, x2 = c1-r1, c1+r1
y1, y2 = c2, c2+r1
dropletBottom = img[y1:y2, x1:x2]       
ret,dropletBottom = cv2.threshold(dropletBottom,20,225,cv2.THRESH_BINARY)
edges = cv2.Canny(dropletBottom, 30, 80)
dropletBottom[edges != 0] = (0, 255, 0)

cv2.imwrite('output/droplet_filled.jpg', dropletBottom)
cv2.imwrite('output/droplet_edges.jpg',edges)
# save('output/edges',edges)
# ========================================================




# Pull out diameter data from edges ================================================
# do least squares with jacobian to find radius
count1 = 0
x = []
y = []

# move through the rows and columns of image matrix and 
# pull out the x and y coordinates of the data
for row in edges:
    count2 = len(edges)
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

# diameter of the droplet!
de           = R_2b*2

# =======================================================================




# Plot data ===============================================================
# plotting functions
plt.close('all')

def plot_all():
    """ Draw data points, best fit circles and center for the three methods,
    and adds the iso contours corresponding to the fiel residu or residu2
    """

    f = plt.figure( facecolor='white')  #figsize=(7, 5.4), dpi=72,
    plt.axis('equal')

    theta_fit = linspace(-pi, pi, 180)

    x_fit2 = xc_2b + R_2b*cos(theta_fit)
    y_fit2 = yc_2b + R_2b*sin(theta_fit)
    plt.plot(x_fit2, y_fit2, 'k--', label=method_2b, lw=2)
    plt.plot([xc_2b], [yc_2b], 'gD', mec='r', mew=1)

    # draw
    plt.xlabel('x (pixels)')
    plt.ylabel('y (pixels)')
    # plot data
    plt.plot(x, y, 'co', label='data', ms=8, mec='c', mew=1)
    plt.legend(loc='best',labelspacing=0.1 )

    # plt.xlim(xmin=vmin, xmax=vmax)
    # plt.ylim(ymin=vmin, ymax=vmax)

    plt.grid()
    plt.title('Least Squares Circle')
    plt.savefig('output/fit_%s.png' % (basename))

plot_all()

# ==================================================














# =========== get the other diameter

count1 = 0
x = []
y = []

# move through the rows and columns of image matrix and 
# pull out the x and y coordinates of the data
for row in fullEdges:
    count2 = len(fullEdges)
    for column in row:
        w = linalg.norm(column)
        if w > 0:
            x.append(count1)
            y.append(count2)
        count2 -= 1
    count1 += 1

x = array(x)
y = array(y)

x_ds = max(x) - de
# find the indices where x < x_ds (this is the part of the
# droplet 'higher' than the diameter of the droplet)
# then clip the y array to only those indices. The max and min 
# should then be the width of the droplet at that point
y_clip = y[where(x<x_ds)]

ds = max(y_clip) - min(y_clip)







# ==== 
# translate diameters from pixels to m
# the needle for water is  0.51 mm
# the needle for hexadecane is 1.85 mm

SMALL = 5
y_clip2 = y[where(x<(min(x)+SMALL))]

needleWidth = max(y_clip2) - min(y_clip2)



y_ds_array = linspace(min(y_clip),max(y_clip),20)
x_ds_array = zeros(20) + x_ds

y_needle = linspace(min(y_clip2),max(y_clip2),5)
x_needle = zeros(5) + min(x)+SMALL

y_de_array = linspace(min(y),max(y),20)
x_de_array = zeros(20) + max(x)-de/2.














def pixels2m(value):
    needleMM = 0.51
    # needleMM = 1.85
    mPerPixel = needleMM/needleWidth*1./1000.
    return value*mPerPixel


ds = pixels2m(ds)
de = pixels2m(de) 

# Summary
print "Droplet diameter = "+str(round(ds*1000,2))+" mm"


# ======== Get surface tension from diameters
s = ds/de

def H_func(s):
    OneOverH = 0.3309*s**(-2.54)
    H = 1/OneOverH
    return H
def gamma_func(H,de):
    rhoAir = 1.2754 #kg/m3
    rhoWater = 999.97 #kg/m3
    deltaRho = rhoAir - rhoWater
    # hexadecane:
    # deltaRho = 768.761 # kg/m3
    g        = 9.8 
    gamma = -deltaRho*g*de**2/H     # N/m
    gamma_mN = gamma * 1000         # mN/m
    return gamma_mN


H = H_func(s)
gamma = gamma_func(H, de)

print "Surface tension: " +str(gamma) + "mN/m"





plt.figure(2)
plt.grid()
plt.title('Droplet w/ diameters')
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('x (pixels)')
plt.ylabel('y (pixels)')
plt.scatter(x,y,
            label='Droplet edges',
            edgecolors = 'c',
            facecolors = 'c',
            alpha = 0.5)
plt.plot(x_de_array,y_de_array,
         label='Droplet diameter',
         color='r',
         linewidth=4)
plt.plot(x_ds_array,y_ds_array,
         label='Throat diameter',
         color='b',
         linewidth=4)
plt.plot(x_needle,y_needle,
         label='Needle width',
         color='g',
         linewidth=4)
plt.legend(loc='best')
plt.savefig('output/droplet_w_diameters.png')
plt.show()















