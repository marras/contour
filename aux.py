#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *

#Auxilliary functions
def read_data (x,y,z,f):
    l = f.readline()
    while l:
        # Detect separator
        if l[0:5] == "-----": return True
        va = l.split()

        x.append(float(va[0]))
        y.append(float(va[1]))
        z.append(float(va[2]))
        l = f.readline()
    return False

def my_logspace(start, end, pts):
    arr = [start]
    step = pow(end/start, 1.0/pts)
    a = start * step
    for i in range(pts):
        arr.append(a)
        a = a * step
    return array(arr)

class MouseHandler:
    event = None
    figure = None
    fp = None
    xdatalist = []
    ydatalist = []

    def __init__(self, fig, fp):
        self.figure = fig
        self.fp = fp

    def on_pick(self, event):
        self.event = event
        self.xdatalist.append(event.xdata)
        self.ydatalist.append(event.ydata)
        print "clicked x = %s and y = %s" % (event.xdata,event.ydata)
        self.fp.write("%s\t%s\n" % (event.xdata, event.ydata))

        ax = self.figure.gca()  # get current axis
        ax.hold(True) # overlay plots.

        # Plot a red circle where you clicked.
        ax.plot([event.xdata],[event.ydata],'ro')

        self.figure.canvas.draw()  # to refresh the plot.
