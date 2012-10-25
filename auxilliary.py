#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *

#Auxilliary functions
def read_data (x,y,z,alpha,f):
    l = f.readline()
    while l:
        # Detect separator
        if l[0:5] == "-----": return True
        va = l.split()

        x.append(float(va[0]))
        y.append(float(va[1]))
        z.append(float(va[2]))
        alpha.append(float(va[-1]))
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

    def __init__(self, fig, fp, left_callback, right_callback):
        self.figure = fig
        self.fp = fp
        self.right_callback = right_callback
        self.left_callback = left_callback

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
        self.left_callback(self.event.xdata, self.event.ydata, self.fp)
    def right_click(self):
        self.right_callback(self.event.xdata, self.event.ydata)
