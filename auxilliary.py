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
    last_x = None
    last_y = None
    num_points = 0

    def __init__(self, fig, fp, redraw_callback):
        self.figure = fig
        self.fp = fp
        self.redraw_callback = redraw_callback

    def on_pick(self, event):
        print "clicked x = %s and y = %s, button = %d" % (event.xdata, event.ydata, event.button)
        self.event = event
        self.xdatalist.append(event.xdata)
        self.ydatalist.append(event.ydata)

        if event.button == 1:
            self.left_click()
        elif event.button == 3:
            self.right_click()

    def left_click(self):
        self.fp.write("%s\t%s\n" % (self.event.xdata, self.event.ydata))

        ax = self.figure.gca()  # get current axis
        ax.hold(True) # overlay plots.

        # Plot a red circle where you clicked.
        ax.plot([self.event.xdata],[self.event.ydata],'ro')
        self.num_points += 1

        if mod(self.num_points,2) == 0:
            # Plot a line to the previous odd point if the current one is even.
            ax.plot([self.last_x,self.event.xdata],[self.last_y,self.event.ydata],'g-')
        else:
            self.last_x, self.last_y = self.event.xdata, self.event.ydata

        self.figure.canvas.draw()  # to refresh the plot.

    def right_click(self):
        self.redraw_callback(self.event.xdata, self.event.ydata)
