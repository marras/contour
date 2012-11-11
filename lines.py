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

class PhaseDiagramGenerator:

    x = []; y = []
    xh = []; yh = []
    fig = None
    num_points = 0

    def __init__(self, filename, pts):
        self.f = open (filename, "rt")
        self.pts = pts
        [self.xh, self.yh] = self.f.readline().split()[:2] #skip header line
        print "Header: ",self.xh,self.yh

    def load_data_and_draw(self):
        self.fig = figure()
        self.x = []; self.y = []
        more_to_come = auxilliary.read_data (self.x,self.y, f=self.f)

        print "min(x)\t max(x)\t min(y)\t max(y)"
        print min(self.x),"\t", max(self.x),"\t", min(self.y),"\t", max(self.y)

        self.grid_and_plot(more_to_come)

    def grid_and_plot(self, more_to_come):

        scatter(self.x,self.y,marker='o',c='b',s=5)

        ###  DRAW LINES HERE ####



        # Set up plot appearance
        xlabel(self.xh)
        ylabel(self.yh)
        title('Mapa S(q_m)')
        xscale('log')
        yscale('log')

        if more_to_come:
            self.load_data_and_draw()

    def start(self):
        self.load_data_and_draw()

        fout = open ("clicks.dat", "wt")
        fout.write("%s\t%s\talpha\n" % (self.xh,self.yh))

        #self.mouse = auxilliary.MouseHandler(self.fig, fout, self.output_click_to_file, self.redraw)
        #self.fig.canvas.mpl_connect('button_press_event', self.mouse.on_pick)

        #self.fig.show()
        while True:
            self.fig.waitforbuttonpress()

print "Generating phase diagram"

cpg = PhaseDiagramGenerator ("dane.dat", 100)
cpg.start()

#import code; code.interact(local=locals()) #TURN ON DEBUGGER



    #def redraw(self, rem_x, rem_y):
        #print "redrawing without x = %f, y = %f..." % (rem_x,rem_y)

        #min_index = self.closest_point_index(rem_x, rem_y)

        #self.x.pop(min_index)
        #self.y.pop(min_index)
        #self.z.pop(min_index)

        #self.fig.clear()
        #self.grid_and_plot(False)

    #def closest_point_index(self, rem_x, rem_y):
        #min_dist = interpol.distance (rem_x, rem_y, self.x[0], self.y[0])
        #min_index = 0
        #for i in range(len(self.x)):
            #dist = interpol.distance (rem_x, rem_y, self.x[i], self.y[i])
            #if dist < min_dist:
                #min_dist = dist
                #min_index = i

        #print "Closest point [%d]: %f, %f" % (min_index, self.x[min_index], self.y[min_index])
        #return min_index

