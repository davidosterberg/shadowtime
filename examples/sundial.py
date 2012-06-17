#!/usr/bin/env python
# coding: utf-8

import shadowtime
from pylab import *
from datetime import date

phi = 14.150704/180*pi
delta = 57.749689/180*pi
h = 1.

xlimits = (-4.8,4.8)
ylimits = (-3,10)

def time_label(hour,x,y):
    global h
    global phi
    global delta
    xx = x[logical_not(isnan(x))]
    yy = y[logical_not(isnan(x))]
    xx = xx[logical_not(isnan(yy))]
    yy = yy[logical_not(isnan(yy))]
    rr = xx**2+yy**2
    try:
        idxmin = argmin(rr)
        xpos = xx[idxmin]
        ypos = yy[idxmin]
        if hour < 12:
            text(xpos-0.05,ypos-0.1,str(hour+2),fontsize=6,\
                horizontalalignment='left',verticalalignment='top')
        else:
            text(xpos+0.05,ypos-0.1,str(hour+2),fontsize=6,\
                horizontalalignment='right',verticalalignment='top')
    except ValueError:
        pass

    dst_start = (datetime.date(2012,3,28) - datetime.date(2012,1,1)).days
    xpos,ypos = shadowtime.shadow(phi,delta,h,(dst_start*24+hour)*3600)
    if xpos and ypos and xpos>xlimits[0] and xpos < xlimits[1]:
        text(xpos,ypos,str(hour+1),fontsize=6,backgroundcolor='w',\
            horizontalalignment='center',verticalalignment='center')
    dst_end = (datetime.date(2012,10,28) - datetime.date(2012,1,1)).days
    xpos,ypos = shadowtime.shadow(phi,delta,h,(dst_end*24+hour)*3600)
    if xpos and ypos and xpos>xlimits[0] and xpos < xlimits[1]:
        text(xpos,ypos,str(hour+1),fontsize=6,backgroundcolor='w',\
            horizontalalignment='center',verticalalignment='center')



figure(num=None, figsize=(11.69, 16.54), dpi=400, facecolor='w', edgecolor='k')
subplot(111, autoscale_on=False,aspect='equal')

for hour in range(24):
    x,y = shadowtime.analemma(phi,delta,h,hour)
    x = x/h
    y = y/h
    plot(x,y,'k',linewidth=0.5)
    time_label(hour,x,y)

for hour in arange(0,24,0.166666666667): 
    x,y = shadowtime.analemma(phi,delta,h,hour)
    x = x/h
    y = y/h
    plot(x,y,'k--',linewidth=0.2,dashes=(2,1))


plot(0,0,'ko')    

# The reference date
Jan1 = date(2012,1,1)

def date_label(s,x,y,xpos):
    global h
    xx = x[logical_not(isnan(x))]
    yy = y[logical_not(isnan(x))]
    xx = xx[logical_not(isnan(yy))]
    yy = yy[logical_not(isnan(yy))]
    ypos = interp(xpos,xx,yy)
    text(xpos[0]-0.1,ypos[0],s,fontsize=6,\
         horizontalalignment='right',verticalalignment='center')
    text(xpos[1]+0.1,ypos[1],s,fontsize=6,\
         horizontalalignment='left',verticalalignment='center')


# Winter solstice
Dec21 = (date(2012,12,21)-Jan1).days
x,y = shadowtime.day_path(phi,delta,h,Dec21)
x = x/h
y = y/h
plot(x,y,'k',linewidth=1.0)
date_label('dec21',x,y,xlimits)

# Equinox
March20 = (date(2012,3,20)-Jan1).days
x,y = shadowtime.day_path(phi,delta,h,March20)
x = x/h
y = y/h
plot(x,y,'k',linewidth=1.0)
date_label('mar20',x,y,xlimits)

# Summer solstice
June20 = (date(2012,6,20)-Jan1).days
x,y = shadowtime.day_path(phi,delta,h,June20)
x = x/h
y = y/h
plot(x,y,'k',linewidth=1.0)
date_label('jun20',x,y,xlimits)

for m in range(12):
    Month1 = date(2012,m+1,1)
    yearday = (Month1-Jan1).days
    x,y = shadowtime.day_path(phi,delta,h,yearday)
    x = x/h
    y = y/h
    plot(x,y,'k',linewidth=0.5)
    date_label(Month1.strftime('%b%d'),x,y,xlimits)


# plot hair cross
plot([-0.5,0.5],[0,0],'k',linewidth=0.5)
text(-0.5,-0.15,u"V",fontsize=6,\
     horizontalalignment='left',verticalalignment='bottom')
text(0.5,-0.15,u"Ö",fontsize=6,\
     horizontalalignment='right',verticalalignment='bottom')
plot([0,0],[-0.3,0],'k',linewidth=0.5)
plot([0,0],[7,8],'k',linewidth=0.5)
text(0,8.05,"N",fontsize=6,\
     horizontalalignment='center',verticalalignment='bottom')


x,y = shadowtime.analemma(phi,delta,h,12)
x = x/h*0.8
x = x-mean(x)-0.3
y = y/h/8.
y = y-mean(y)
plot(x,y-1.2,'k',linewidth=0.5)
text(-0.4,-0.8,"Normaltid",fontsize=6,\
     horizontalalignment='center',verticalalignment='bottom')
text(0.4,-1.2,"Sommartid",fontsize=6,\
     horizontalalignment='center',verticalalignment='bottom')
dx = -0.08+0.1
dy = -5.54
arrowhead = 0.15*array([[0+dx,0+dy],[0.7+dx,0.2+dy],[0.45+dx,0.45+dy]])
gca().add_patch(Polygon(arrowhead,True,facecolor='k',linewidth=0.5))
plot([-0.7,0.6],[-1.3,-0.8],'k',linewidth=0.2)

def classical_degree_notation(angle):
    degree = int(angle)
    minute = int((angle - degree)*60)
    second = int((angle-degree-minute/60.)*3600)
    dic = {"degree":degree,"minute":minute,"second":second}
    return u"""%(degree)d${}^\circ$%(minute)02d' %(second)02d""" % dic + '"'   #" this is to trick vim

def classic_position(lat,lon):
    s = classical_degree_notation(lat)
    if lat > 0:
        s = s + " N, "
    else:
        s = s + " S, "
    s = s + classical_degree_notation(lon)
    if lon > 0:
        s = s + " E"
    else:
        s = s + " W"
    return s

def description(xpos,ypos):
    phi = 14.150704/180*pi
    delta = 57.749689/180*pi
    h = 1.

    R=6371e3
    alpha = 23.44/180*pi
    beta = 2*pi/(1.000017421*365.25*24*3600)  # source wikipedia
    Omega = 2*pi/86164.1
    solstice_offset = -10*24*3600 # winter solstice offset (januari 1) - (december 21)
    e=0.01671123

    s = "Solurets position:\n"
    s += "Tidszon:\n"
    s += "Jordens rotationstid:\n"
    s += "Jordaxelns lutning:\n"
    s += "Omloppsperioden:\n"
    s += "Omloppsbanans eccentricitet:\n"
    s += u"Ingen justering för sommartid har gjorts\n"
    text(xpos,ypos,s,verticalalignment='top',horizontalalignment='left',fontsize=6,color='k')
    s = classic_position(delta*180/pi,phi*180/pi) + "\n"
    s += "+3600 sekunder\n"
    s += str(2*pi/Omega) + " sekunder\n"
    s += classical_degree_notation(alpha*180/pi)+"\n"
    s += str(2*pi/beta) + " sekunder\n"
    s += str(e) +"\n"
    s += "\n"
    text(-xpos,ypos,s,verticalalignment='top',horizontalalignment='right',fontsize=6,color='k')


description(-1.1,-1.7)

xlim(xlimits)
ylim(ylimits)
axis('off')

savefig("sundial_jonkoping.pdf",dpi=150)#,bbox_inches='tight')
#show()
