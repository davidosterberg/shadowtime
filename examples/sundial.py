#!/usr/bin/env python

import shadowtime
from pylab import *

phi = -127./180*pi
delta = 36.4/180*pi
h = 1.

for hour in range(24): 
    x,y = shadowtime.analemma(phi,delta,h,hour)
    x = x/h
    y = y/h
    x[x < -4] = None
    y[x < -4] = None
    x[x > 4] = None
    y[x > 4] = None    
    plot(x,y,'k')

plot(0,0,'ko')    

x,y = shadowtime.day_path(phi,delta,h,365-shadowtime.solstice_offset)
x = x/h
y = y/h

x[x < -4] = None
y[x < -4] = None
x[x > 4] = None
y[x > 4] = None 
plot(x,y,'k',linewidth=2.0)
x,y = shadowtime.day_path(phi,delta,h,365/2-shadowtime.solstice_offset)
x = x/h
y = y/h

x[x < -4] = None
y[x < -4] = None
x[x > 4] = None
y[x > 4] = None 
plot(x,y,'k',linewidth=2.0)

show()
