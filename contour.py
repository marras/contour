#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
from numpy.random import *
from scipy import *
from scipy.interpolate import griddata
from matplotlib.pyplot import *
import wx
import interpol
import auxilliary
import sys

class ContourPlotGenerator:

    x = []; y = []; z = []; alpha = []
    xh = []; yh = []; zh = []
    fig = None
    title = "S(qm) heightmap"
    num_points = 0

    def __init__(self, filename, pts, title, auto = False):
        self.f = open (filename, "rt")
        self.pts = pts
        self.title = title
        self.auto = auto
        [self.xh, self.yh, self.zh] = self.f.readline().split()[:3] #skip header line
        print "Header: ",self.xh,self.yh,self.zh

    def load_data_and_draw(self):
        self.fig = figure()
        self.x = []; self.y = []; self.z = []
        more_to_come = auxilliary.read_data (self.x,self.y,self.z,self.alpha,self.f)

        print "min(x)\t max(x)\t min(y)\t max(y)"
        print min(self.x),"\t", max(self.x),"\t", min(self.y),"\t", max(self.y)

        self.grid_and_plot(more_to_come)

    def grid_and_plot(self, more_to_come):
        # Grid the data
        xi = auxilliary.my_logspace(min(self.x),max(self.x),self.pts)
        yi = auxilliary.my_logspace(min(self.y),max(self.y),self.pts)

        # For sensible interpolation we need to temporarily get rid of the Log scale
        xi_lin = array([ math.log(a) for a in xi ])
        yi_lin = array([ math.log(a) for a in yi ])
        x_lin = array([ math.log(a)  for a in self.x ])
        y_lin = array([ math.log(a)  for a in self.y ])

        # Custom interpolation routine (defined in interpol.py)
        #zi = interpol.my_griddata((x, y), z, (xi[None,:], yi[:,None])) #non-linearized version
        # Builtin interpolation (SciPy)
        zi = griddata((x_lin, y_lin), self.z, (xi_lin[None,:], yi_lin[:,None]), method='linear') #'cubic', 'linear'

        # contour the gridded data.
        levels = arange(0.1, 5.1, 0.3) # Boost the upper limit to avoid truncation

        CS = contour(xi,yi,zi,15,linewidths=0.5,colors='k')
        CS = contourf(xi,yi,zi,15,cmap=cm.jet, levels=levels)
        colorbar() # draw colorbar
        scatter(self.x,self.y,marker='o',c='b',s=5)

        if more_to_come:
            print "Error: requested to create a contour plot with multiple data sets! Drawing only first one."
            return

        CS = contour(xi,yi,zi, (3.1,), colors = 'k', linewidths = 3, hold='on')

        # Set up plot appearance
        xlabel(self.xh)
        ylabel(self.yh)
        title(self.title)
        xscale('log')
        yscale('log')

        if more_to_come:
            self.load_data_and_draw()

    def output_click_to_file(self, xdata, ydata, fp):
        min_index = self.closest_point_index(xdata, ydata)
        fp.write("%s\t%s\t%s\n" % (xdata, ydata, self.alpha[min_index]))

        ax = self.fig.gca()  # get current axis
        ax.hold(True) # overlay plots.

        # Plot a red circle where you clicked.
        ax.plot([xdata],[ydata],'ro')
        self.num_points += 1

        if mod(self.num_points,2) == 0:
            # Plot a line to the previous odd point if the current one is even.
            ax.plot([self.last_x,xdata],[self.last_y,ydata],'g-')
        else:
            self.last_x, self.last_y = xdata, ydata

        self.fig.canvas.draw()  # to refresh the plot.

    def redraw(self, rem_x, rem_y):
        print "redrawing without x = %f, y = %f..." % (rem_x,rem_y)

        min_index = self.closest_point_index(rem_x, rem_y)

        self.x.pop(min_index)
        self.y.pop(min_index)
        self.z.pop(min_index)

        self.fig.clear()
        self.grid_and_plot(False)

    def closest_point_index(self, rem_x, rem_y):
        min_dist = interpol.distance (rem_x, rem_y, self.x[0], self.y[0])
        min_index = 0
        for i in range(len(self.x)):
            dist = interpol.distance (rem_x, rem_y, self.x[i], self.y[i])
            if dist < min_dist:
                min_dist = dist
                min_index = i

        print "Closest point [%d]: %f, %f" % (min_index, self.x[min_index], self.y[min_index])
        return min_index

    def start(self):
        self.load_data_and_draw()

        fout = open ("clicks.dat", "wt")
        fout.write("%s\t%s\talpha\n" % (self.xh,self.yh))

        self.mouse = auxilliary.MouseHandler(self.fig, fout, self.output_click_to_file, self.redraw)
        self.fig.canvas.mpl_connect('button_press_event', self.mouse.on_pick)

        self.fig.show()
        if self.auto:
          self.fig.savefig('Fig.png')
        else:
          while True:
            self.fig.waitforbuttonpress()

tit = ""
auto = False

if len(sys.argv) > 1:
    a = sys.argv[1].split('_')
    tit = "%s = %s, %s = %s" % (a[0], a[1], a[2], a[3])
    auto = True
else:
    print "Generating contour plot for S(qm): dane.dat"

cpg = ContourPlotGenerator ("dane.dat", 100, tit, auto)
cpg.start()

#import code; code.interact(local=locals()) #TURN ON DEBUGGER
