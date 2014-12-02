#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://www.scipy.org/Cookbook/Least_Squares_Circle
"""
from matplotlib                 import pyplot as plt, cm, colors
from numpy import *
from scipy      import optimize


# Decorator to count functions calls
import functools
def countcalls(fn):
    "decorator function count function calls "

    @functools.wraps(fn)
    def wrapped(*args):
        wrapped.ncalls +=1
        return fn(*args)

    wrapped.ncalls = 0
    return wrapped



# === load data from image edges ===
matrix = load('output/edges.npy')
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

#  == METHOD 2 ==
# Basic usage of optimize.leastsq
# method_2  = "leastsq"

# def calc_R(xc, yc):
#     """ calculate the distance of each 2D points from the center (xc, yc) """
#     return sqrt((x-xc)**2 + (y-yc)**2)

# @countcalls
# def f_2(c):
#     """ calculate the algebraic distance between the 2D points and the mean circle centered at c=(xc, yc) """
#     Ri = calc_R(*c)
#     return Ri - Ri.mean()

# center_estimate = x_m, y_m
# center_2, ier = optimize.leastsq(f_2, center_estimate)

# xc_2, yc_2 = center_2
# Ri_2       = calc_R(xc_2, yc_2)
# R_2        = Ri_2.mean()
# residu_2   = sum((Ri_2 - R_2)**2)
# residu2_2  = sum((Ri_2**2-R_2**2)**2)
# ncalls_2   = f_2.ncalls

# == METHOD 2b ==
# Advanced usage, with jacobian
method_2b  = "leastsq with jacobian"

def calc_R(xc, yc):
    """ calculate the distance of each 2D points from the center c=(xc, yc) """
    return sqrt((x-xc)**2 + (y-yc)**2)

@countcalls
def f_2b(c):
    """ calculate the algebraic distance between the 2D points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(*c)
    return Ri - Ri.mean()

@countcalls
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
residu_2b    = sum((Ri_2b - R_2b)**2)
residu2_2b   = sum((Ri_2b**2-R_2b**2)**2)
ncalls_2b    = f_2b.ncalls

print """
Method 2b :
print "Functions calls : f_2b=%d Df_2b=%d""" % ( f_2b.ncalls, Df_2b.ncalls)



# Summary
fmt = '%-22s %10.5f %10.5f %10.5f %10d %10.6f %10.6f %10.2f'
print ('\n%-22s' +' %10s'*7) % tuple('METHOD Xc Yc Rc nb_calls std(Ri) residu residu2'.split())
print '-'*(22 +7*(10+1))

# print  fmt % (method_2 , xc_2 , yc_2 , R_2 , ncalls_2 , Ri_2.std() , residu_2 , residu2_2 )
print  fmt % (method_2b, xc_2b, yc_2b, R_2b, ncalls_2b, Ri_2b.std(), residu_2b, residu2_2b)


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
    plt.xlabel('x')
    plt.ylabel('y')

    # # plot the residu fields
    # nb_pts = 100

    # plt.draw()
    # xmin, xmax = plt.xlim()
    # ymin, ymax = plt.ylim()

    # vmin = min(xmin, ymin)
    # vmax = max(xmax, ymax)

    # xg, yg = ogrid[vmin:vmax:nb_pts*1j, vmin:vmax:nb_pts*1j]
    # xg = xg[..., newaxis]
    # yg = yg[..., newaxis]

    # Rig    = sqrt( (xg - x)**2 + (yg - y)**2 )
    # Rig_m  = Rig.mean(axis=2)[..., newaxis]

    # if residu2 : residu = sum( (Rig**2 - Rig_m**2)**2 ,axis=2)
    # else       : residu = sum( (Rig-Rig_m)**2 ,axis=2)

    # lvl = exp(linspace(log(residu.min()), log(residu.max()), 15))

    # plt.contourf(xg.flat, yg.flat, residu.T, lvl, alpha=0.4, cmap=cm.Purples_r) # , norm=colors.LogNorm())
    # cbar = plt.colorbar(fraction=0.175, format='%.f')
    # plt.contour (xg.flat, yg.flat, residu.T, lvl, alpha=0.8, colors="lightblue")

    # if residu2 : cbar.set_label('Residu_2 - algebraic approximation')
    # else       : cbar.set_label('Residu')

    # plot data
    plt.plot(x, y, 'ro', label='data', ms=8, mec='b', mew=1)
    plt.legend(loc='best',labelspacing=0.1 )

    # plt.xlim(xmin=vmin, xmax=vmax)
    # plt.ylim(ymin=vmin, ymax=vmax)

    plt.grid()
    plt.title('Least Squares Circle')
    plt.savefig('output/fit_%s.png' % (basename))

plot_all()

plt.show()
# vim: set et sts=4 sw=4:












