#/usr/bin/env python3
# -*- encoding: utf-8-*-

from __future__ import division, unicode_literals, print_function
from pylab import *
import csv
import easygui
import matplotlib
import sympy

def get_magnetic_field(i, rx, ry, mu0=4*pi*1e-7, mu=1):
    r = sqrt(rx**2 + ry**2)
    B = mu0*mu*i/r
    By = B*rx/r
    Bx = -B*ry/r
    return Bx, By    

class Conductor():
    x = 0
    y = 0
    i = 0
    name = ''
    def __init__(self, x=0, y=0, i=0, name=''):
        self.x = x
        self.y = y
        self.i = i
        self.name = name
    def magnetic_field(self, x, y):
        Bx, By = get_magnetic_field(self.i, x-self.x, y-self.y)
        return Bx, By

class ConductorPlane():
    Bxx = []
    Byy = []
    Babs = []
    conductors = []
    lookup_table = []
    def __init__(self, x, y):
        self.Babs = zeros((len(x), len(y)))
        self.Bxx = zeros((len(x), len(y)))
        self.Byy = zeros((len(x), len(y)))
    def add_conductor(self, c):
        self.conductors.append(c)
    def get_magnetic_field(self):
        Bxx = self.Bxx
        Byy = self.Byy
        Babs = self.Babs
        for c in self.conductors:
            for i in range(0, len(x)):
                for j in range (0, len(y)):
                    Bx, By = c.magnetic_field(x[i], y[j])
                    Bxx[i,j] += Bx
                    Byy[i,j] += By
        for i in range(0, len(x)):
            for j in range(0, len(y)):
                Babs[i,j] = sqrt(Bxx[i,j]**2 + Byy[i,j]**2)
        return Babs, Bxx, Byy
    def read_from_file(self, filename):
        with open (filename) as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                x = float(sympy.sympify(row['x']))
                y = float(sympy.sympify(row['y']))
                i = float(sympy.sympify(row['i']))
                name = str(row['name'])
                self.add_conductor(Conductor(x, y, i, name))

# Define the plane where the magnetic field is to be calculated
x = linspace(-50, 50, 1e3)
y = linspace(-10, 30, 1e3)
p = ConductorPlane(x, y)
# Read a source file
filename = easygui.fileopenbox()
p.read_from_file(filename)
# Calculate magnetic field
Babs, Bxx, Byy = p.get_magnetic_field()
# Plot the magnetic field
pcolormesh(x, y, Babs.transpose()*1e6, cmap=cm.Blues, vmin=0, vmax=300)
colorbar()
w = array([(max(y)-min(y))/(max(x)-min(x)), 1])
streamplot(x, y, Bxx.transpose()*1e6, Byy.transpose()*1e6, density=w*3, color='black')
cs = contour(x, y, Babs.transpose()*1e6, logspace(log10(0.4), log10(300), 10), colors='grey')
clabel(cs, fmt='%1.1f')
csRef = contour(x, y, Babs.transpose()*1e6, [300], colors='red')
clabel(csRef, fmt='%1.1f')
grid(True)
hlines(0, min(x), max(x), color='green')
axis('tight')
axis('scaled')
xlabel('Avstand fra spormidten, m')
ylabel('Høyde over skinneoverkant, m')
for c in p.conductors:
    plot(c.x, c.y, 'o', color='red')
    if c.i > 0:
        plot(c.x, c.y, '.', color='red')
    if c.i < 0:
        plot(c.x, c.y, 'x', color='red')
show()
