#!/usr/bin/env python

import shadowtime
from pylab import *

phi = 14.150704/180*pi
delta = 57.749689/180*pi
h = 1.

subplot(111, autoscale_on=False,aspect='equal')
for hour in range(24): 
    x,y = shadowtime.analemma(phi,delta,h,hour)
    x = x/h
    y = y/h
    plot(x,y,'k')

plot(0,0,'ko')    

x,y = shadowtime.day_path(phi,delta,h,365+shadowtime.solstice_offset)
x = x/h
y = y/h

plot(x,y,'k',linewidth=2.0)
x,y = shadowtime.day_path(phi,delta,h,365/2+shadowtime.solstice_offset)
x = x/h
y = y/h

plot(x,y,'k',linewidth=2.0)
plot([-0.5,0.5],[-1,-1],'k')
plot([-0.5,0.5],[-2,-2],'k')
plot([-0.5,-0.5],[-2,-1],'k')
plot([0.5,0.5],[-2,-1],'k')

xlim((-12,12))
ylim((-12,18))
axis('off')
show()
