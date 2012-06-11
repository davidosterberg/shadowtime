#!/usr/bin/env python
""" Verification using an analemma found on the web """

import shadowtime
from pylab import *

phi = -127./180*pi
delta = 36.4/180*pi
h = 1.

#fig = figure()
im = imread("CupidoSunShadowPlot.jpg")
imshow(im,origin='lower',interpolation='nearest');
plot([51,682],[65,520],'ro')

# some code to find the transformation to image coordinates
A = array([[1,-4.],[1,4.]])
b = array([51.,682.])
tx  = solve(A,b)
A = array([[1,-4.],[1,4.]])
b = array([65.,520.])
ty  = solve(A,b)
Tx = lambda x: tx[0]+tx[1]*x
Ty = lambda y: ty[0]+ty[1]*y  

for hour in [2,16,17,18,19,20,21,22,23,24]:
    x,y = shadowtime.analemma(phi,delta,h,hour)
    x = x/h
    y = y/h
    x[x < -4] = None
    y[x < -4] = None
    x[x > 4] = None
    y[x > 4] = None    
    plot(Tx(x),Ty(y),'k')

plot(Tx(0),Ty(0),'ks')    
axis('off')


x,y = shadowtime.day_path(phi,delta,h,365)
x = x/h
y = y/h

x[x < -4] = None
y[x < -4] = None
x[x > 4] = None
y[x > 4] = None 
plot(Tx(x),Ty(y),'k',linewidth=2.0)
x,y = shadowtime.day_path(phi,delta,h,365/2)
x = x/h
y = y/h

x[x < -4] = None
y[x < -4] = None
x[x > 4] = None
y[x > 4] = None 
plot(Tx(x),Ty(y),'k',linewidth=2.0)

show()
