#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
from numpy.random import *
from scipy import *
from scipy.interpolate import griddata
from matplotlib.pyplot import *
import interpol

#Settings
pts = 100

def max (lst):
    max = lst[0]
    for i in lst[1:]:
        if i > max: max = i
    return max
def min (lst):
    min = lst[0]
    for i in lst[1:]:
        if i < min: min = i
    return min

f = open ("dane.dat", "rt")

x = []
y = []
z = []

rx = []
ry = []
rz = []

[xh, yh, zh] = f.readline().split()[:3] #skip header line
print "Header: ",xh,yh,zh

for l in f.readlines():
    va = l.split()

    x.append(float(va[0]))
    y.append(float(va[1]))
    z.append(float(va[2]))

print "min(x)\t max(x)\t min(y)\t max(y)"
print min(x),"\t", max(x),"\t", min(y),"\t", max(y)

def my_logspace(start, end, pts):
    arr = [start]
    step = pow(end/start, 1.0/pts)
    a = start * step
    while a <= end:
        arr.append(a)
        a = a * step
    return array(arr)

# Grid the data

xi = my_logspace(min(x),max(x),pts)
yi = my_logspace(min(y),max(y),pts)

# For sensible interpolation we need to temporarily get rid of the Log scale
xi_lin = array([ math.log(a) / math.log(max(x))  for a in xi ])
yi_lin = array([ math.log(a) / math.log(max(y))  for a in yi ])
x_lin = array([ math.log(a) / math.log(max(x))  for a in x ])
y_lin = array([ math.log(a) / math.log(max(y))  for a in y ])

# Builtin interpolation (SciPy)
#zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='linear') #'cubic', 'linear'
#zi = griddata((x_lin, y_lin), z, (xi_lin[None,:], yi_lin[:,None]), method='linear') #'cubic', 'linear'

# Custom interpolation routine (defined in interpol.py)
#zi = interpol.my_griddata((x, y), z, (xi[None,:], yi[:,None])) #non-linearized version
zi = interpol.my_griddata((x_lin, y_lin), z, (xi_lin[None,:], yi_lin[:,None])) #'cubic', 'linear'

# contour the gridded data.
levels = arange(0.1, 5.1, 0.3) # Boost the upper limit to avoid truncation

CS = contour(xi,yi,zi,15,linewidths=0.5,colors='k')
CS = contourf(xi,yi,zi,15,cmap=cm.jet, levels=levels)
colorbar() # draw colorbar

CS = contour(xi,yi,zi, (3.1,), colors = 'k', linewidths = 3, hold='on')

# Plot data points
scatter(x,y,marker='o',c='b',s=5)

X = array(x)
Y = array(y)
Z = array(z)

xlabel(xh)
ylabel(yh)
title('Mapa S(q_m)')

xscale('log')
yscale('log')
show()

#import code; code.interact(local=locals()) #TURN ON DEBUGGER
