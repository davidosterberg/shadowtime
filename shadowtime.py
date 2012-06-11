#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple GUI for shadow flicker calculations.
Use this code at your own risk!

## Usage:
Just run
>python2 shadow_gui.py


## Website:
https://github.com/davidosterberg/shadowtime

## Licence:
(C) 2012 David Österberg

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from pylab import *
from matplotlib.nxutils import points_inside_poly
import sys

# Earth parameters
R=6371e3
alpha = 23.44/180*pi
beta = 2*pi/(1.000017421*365.25*24*3600)  # source wikipedia
Omega = 2*pi/86164.1
solstice_offset = -10*24*3600 # winter solstice offset (januari 1) - (december 21) 

def point_shadow(p):
    """ Returns the shadow of a point on a sphere centered in (0,0,0). 
    global variable R is the radius of the sphere an p is the cartesian
    coordinates of the point. """
    global R
    c = -array(p).flatten()
    v = array([0,-1,0])
    xx = dot(v,c)**2-dot(c,c)+R**2
    if xx < 0:
        return None
    d = dot(v,c) - xx**0.5
    if d < 0:
        return None
    else:
        return p+d*v

def Rx(t):
    """ Rotation matrix for t radians about x-axis  """
    return matrix([[1,0,0],[0,cos(t),-sin(t)],[0,sin(t),cos(t)]])

def Ry(t):
    """ Rotation matrix for t radians about y-axis  """
    return matrix([[cos(t),0,sin(t)],[0,1,0],[-sin(t),0,cos(t)]])

def Rz(t):
    """ Rotation matrix for t radians about y-axis  """
    return matrix([[cos(t),-sin(t),0],[sin(t),cos(t),0],[0,0,1]])

def Geographical_to_Earth_Cartesian(phi,delta,h):
    """ Transformation from geographic coordinates to a earth locked 
    cartesian coordinates with origo in the earth center. """
    global R
    return matrix([[(R+h)*sin(pi/2-delta)*cos(phi)],\
                   [(R+h)*sin(pi/2-delta)*sin(phi)],\
                   [(R+h)*cos(pi/2-delta)]])


def orbital_position(t):
    """ Give the position of earth on the orbit as an angle """
    return 2*pi*7.66/(24*60)*sin(beta*t)+beta*t

def Earth_Cartesian_to_Geographical(xyz):
    """ Transformation from earth locked cartesian coordinates with 
    origo in the earth center into geographic coordinates. """
    global R
    r = norm(xyz)
    x = xyz[0,0]
    y = xyz[1,0]
    z = xyz[2,0]
    return arctan2(y,x),pi/2-arccos(z/r),r-R

def Geographical_to_Universal(phi,delta,h,t):
    """ Transformation from geographic coordinates to coordinates
    with origo in the earth center, the axes locked to the stars 
    and the xy-plane in the orbital plane. """
    global R
    global alpha
    global beta
    global Omega
    global solstice_offset
    t += solstice_offset
    return Rz(-orbital_position(t))*Rx(alpha)*Rz(Omega*t-pi/2)*Geographical_to_Earth_Cartesian(phi,delta,h)

def Universal_to_Geographical(XYZ,t):
    """ Transformation from a coordinate system with origo in the 
    earth center, the axes locked to the stars and the xy-plane in 
    the orbital plane, into geographic coordinates. """
    global R
    global alpha
    global beta
    global Omega
    global solstice_offset
    t += solstice_offset
    xyz = inv(Rz(-orbital_position(t))*Rx(alpha)*Rz(Omega*t-pi/2))*XYZ
    return Earth_Cartesian_to_Geographical(xyz)

def shadow_box(width,tip_xy):
    """ Returns the vertices of an inclined rectangle where one side
    (of length width) is centered in origo and the opposing side is 
    centered in tip_xy. """
    box_width = width
    box_length = norm(tip_xy)
    box_inclination = -arctan2(float(tip_xy[0]),tip_xy[1])
    box_upright = array([[-box_width/2.,0],\
                         [box_width/2.,0], \
                         [box_width/2.,box_length],\
                         [-box_width/2.,box_length]])
    rotation_matrix = array([[cos(box_inclination),-sin(box_inclination)],\
                             [sin(box_inclination),cos(box_inclination)]])
    box_inclined = transpose(dot(rotation_matrix,transpose(box_upright)))
    return box_inclined



def points_in_box(X,Y,box):
    """ Given a grid X,Y as given by meshgrid and a list of vertices
    of a rectangle (or any four sided polygon) return the grid points
    inside the box and the indices of these grid points. """
    xx = X.flatten()
    yy = Y.flatten()
    xypoints = [(xx[k],yy[k]) for k in range(len(xx))]
    xyverts = [(box[k,0],box[k,1]) for k in range(4)]
    inside = points_inside_poly(xypoints,xyverts)
    xyin = array(xypoints)[inside]
    inside.shape = X.shape
    return xyin,inside

def tower_shadow_map(phi,delta,h,diameter,t,X,Y,progress_queue,cancel_event):
    """ Given a grid X,Y as given by meshgrid, a location on the earth
    surface given by (phi,delta), a tower of height h and of a certain
    diameter, a time vector t (in seconds), return the number of
    seconds the grid points are in shadow by the tower."""
    global R
    shadow_time = zeros(X.shape)
    for k in range(len(t)):
        if (k % (24*60)) == 0:
            progress_queue.put(float(k)/len(t))
            if cancel_event.isSet():
                return None
        pXYZ = Geographical_to_Universal(phi,delta,h,t[k])
        sXYZ = transpose(matrix(point_shadow(array(pXYZ).flatten())))
        if sXYZ[0,0] != None:
            sphi,sdelta,sh = Universal_to_Geographical(sXYZ,t[k])
            box = shadow_box(diameter,((sphi-phi)*R*cos(delta),(sdelta-delta)*R))
            xyin,inside = points_in_box(X,Y,box)
            shadow_time[inside] += 60.
    progress_queue.put(1.0)
    return shadow_time

def day_path(phi,delta,h,n):
    """ Returns the trace of a shadow for a given day """ 
    global Omega
    global R
    global beta
    t0 = n*24*3600
    t = linspace(t0,t0+24*3600,24*60)
    sphis = zeros(len(t))
    sdeltas = zeros(len(t))
    for k in range(len(t)):
        pXYZ = Geographical_to_Universal(phi,delta,h,t[k])
        sXYZ = transpose(matrix(point_shadow(array(pXYZ).flatten())))
        if sXYZ[0,0] != None:
            sphi,sdelta,sh = Universal_to_Geographical(sXYZ,t[k])
            sphis[k] = sphi
            sdeltas[k] = sdelta
        else:
            sphis[k] = None
            sdeltas[k] = None
    return (sphis-phi)*R*cos(delta),(sdeltas-delta)*R

def analemma(phi,delta,h,hour_utc):
    """ return the shadow analemma for a certain hour (UTC)"""
    global R
    t0 = hour_utc*3600
    t = arange(t0,t0+366*24*3600,24*3600)
    sphis = zeros(len(t))
    sdeltas = zeros(len(t))

    for k in range(len(t)):
        pXYZ = Geographical_to_Universal(phi,delta,h,t[k])
        sXYZ = transpose(matrix(point_shadow(array(pXYZ).flatten())))
        if sXYZ[0,0] != None:
            sphi,sdelta,sh = Universal_to_Geographical(sXYZ,t[k])
            sphis[k] = sphi
            sdeltas[k] = sdelta
        else:
            sphis[k] = None
            sdeltas[k] = None
    return (sphis-phi)*R*cos(delta),(sdeltas-delta)*R
