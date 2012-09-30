#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
from numpy.random import *
from scipy import *
from scipy.interpolate import griddata
from matplotlib.pyplot import *
import wx
import interpol
import aux
import sys

if len(sys.argv) > 1:
    if sys.argv[1] == '--line': only_line = True
    print "Generating line phase diagram"
else:
    only_line = False
    print "Generating contour plot for S(qm)"

#Settings
pts = 100

f = open ("dane.dat", "rt")

[xh, yh, zh] = f.readline().split()[:3] #skip header line
print "Header: ",xh,yh,zh

def prepare_graph():
    x = []; y = []; z = []
    more_to_come = aux.read_data (x,y,z,f)

    print "min(x)\t max(x)\t min(y)\t max(y)"
    print min(x),"\t", max(x),"\t", min(y),"\t", max(y)

    # Grid the data
    xi = aux.my_logspace(min(x),max(x),pts)
    yi = aux.my_logspace(min(y),max(y),pts)

    # For sensible interpolation we need to temporarily get rid of the Log scale
    xi_lin = array([ math.log(a) for a in xi ])
    yi_lin = array([ math.log(a) for a in yi ])
    x_lin = array([ math.log(a)  for a in x ])
    y_lin = array([ math.log(a)  for a in y ])

    # Custom interpolation routine (defined in interpol.py)
    #zi = interpol.my_griddata((x, y), z, (xi[None,:], yi[:,None])) #non-linearized version
    # Builtin interpolation (SciPy)
    zi = griddata((x_lin, y_lin), z, (xi_lin[None,:], yi_lin[:,None]), method='linear') #'cubic', 'linear'

    # contour the gridded data.
    levels = arange(0.1, 5.1, 0.3) # Boost the upper limit to avoid truncation

    if not only_line:
        CS = contour(xi,yi,zi,15,linewidths=0.5,colors='k')
        CS = contourf(xi,yi,zi,15,cmap=cm.jet, levels=levels)
        colorbar() # draw colorbar
        scatter(x,y,marker='o',c='b',s=5)

        if more_to_come:
            print "Error: requested to create a contour plot with multiple data sets! Drawing only first one."
            return

    CS = contour(xi,yi,zi, (3.1,), colors = 'k', linewidths = 3, hold='on')

    if more_to_come:
        prepare_graph()

fig = figure()
prepare_graph()

xlabel(xh)
ylabel(yh)
title('Mapa S(q_m)')
xscale('log')
yscale('log')

fout = open ("clicks.dat", "wt")
fout.write("%s\t%s\n" % (xh,yh))

mouse = aux.MouseHandler(fig, fout)
fig.canvas.mpl_connect('button_press_event', mouse.on_pick)

fig.show()
while True:
    fig.waitforbuttonpress()

#import code; code.interact(local=locals()) #TURN ON DEBUGGER
