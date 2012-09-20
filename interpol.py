from numpy import *
from math import sqrt

power = 6

# x,y - actual data
# xi,yi - logspace grid points
def my_griddata((x, y), z, (xi, yi)):

    #import code; code.interact(local=locals()) #TURN ON DEBUGGER
    out = []
    for py in yi:
        for px in xi[0]:
            interpolated_z = z_value (px,py, x,y,z)
            out.append(interpolated_z)
    return array(out).reshape(len(xi[0]), len(yi))

def z_value(px,py, x,y,z):
    weights = []
    for i in range(len(x)):
        dist = distance (px, py, x[i], y[i])
        if dist > 0:
            weights.append(1 / dist**power)
        else: return z[i]

    total_weight = 0.0
    for w in weights:
        total_weight += w

    total_z = 0.0
    for i in range(len(x)):
        total_z += z[i] * weights[i] / total_weight

    return total_z

def distance(a,b, x,y):
    dx = a-x
    dy = b-y
    return sqrt(dx*dx + dy*dy)
