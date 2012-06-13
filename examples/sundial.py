#!/usr/bin/env python

import shadowtime
from pylab import *
from datetime import date

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

# The reference date
Jan1 = date(2012,1,1)

# Winter solstice
Dec21 = (date(2012,12,21)-Jan1).days
x,y = shadowtime.day_path(phi,delta,h,Dec21)
x = x/h
y = y/h
plot(x,y,'k',linewidth=2.0)

# Equinox
March20 = (date(2012,3,20)-Jan1).days
x,y = shadowtime.day_path(phi,delta,h,March20)
x = x/h
y = y/h
plot(x,y,'k',linewidth=2.0)

# Summer solstice
June20 = (date(2012,6,20)-Jan1).days
x,y = shadowtime.day_path(phi,delta,h,June20)
x = x/h
y = y/h
plot(x,y,'k',linewidth=2.0)

# plot grid square
plot([-0.5,0.5],[-1,-1],'k')
plot([-0.5,0.5],[-2,-2],'k')
plot([-0.5,-0.5],[-2,-1],'k')
plot([0.5,0.5],[-2,-1],'k')

xlim((-12,12))
ylim((-12,18))
axis('off')
show()
