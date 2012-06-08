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

import matplotlib
matplotlib.use("TkAgg")
from pylab import *
from Tkinter import Frame,Entry,Label,Button,W,SW,E
from progressmeter import Meter
import Queue
import threading
import shadow

class App(Frame):

    def __init__(self, master=None):
        self.computing = False
        self.S = None

        self.progress_queue = Queue.Queue()
        self.cancel_event = threading.Event()

        Frame.__init__(self, master)
        self.grid()
        self.master.protocol("WM_DELETE_WINDOW", self.close_handler)

        w = Label(self,text=" ",fg="red")
        w.grid(row=0,column=0,pady=10,sticky=W)

        ## Object parameters
        w = Label(self,text="Tower parameters:",fg="red")
        w.grid(row=0,column=1,pady=10,sticky=W)

        w = Label(self,text="Latitude (deg):")
        w.grid(row=1,column=1,sticky=W)
        self.lat_ent = Entry(self,width=36)
        self.lat_ent.grid(row=1,column=2,sticky=W)
        self.lat_ent.insert(0, "60")

        w = Label(self,text="Tower height (m):")
        w.grid(row=2,column=1,sticky=W)
        self.height_ent = Entry(self,width=36)
        self.height_ent.grid(row=2,column=2,sticky=W)
        self.height_ent.insert(0, "50")

        w = Label(self,text="Tower diameter (m):")
        w.grid(row=3,column=1,sticky=W)
        self.diam_ent = Entry(self,width=36)
        self.diam_ent.grid(row=3,column=2,sticky=W)
        self.diam_ent.insert(0, "30")

        ## Simulation parameters
        w = Label(self,text="Simulation parameters",fg="red")
        w.grid(row=4,column=1,pady=10,sticky=SW)

        w = Label(self,text="Time vector (s):")
        w.grid(row=5,column=1,sticky=W)
        self.time_ent = Entry(self,width=36)
        self.time_ent.grid(row=5,column=2)
        self.time_ent.insert(0, "arange(0,365*24*3600,10*60)")


        ## Output parameters
        w = Label(self,text="Output parameters",fg="red")
        w.grid(row=6,column=1,pady=10,sticky=SW)

        w = Label(self,text="East-west grid (m):")
        w.grid(row=7,column=1,sticky=W)
        self.gridx_ent = Entry(self,width=36)
        self.gridx_ent.grid(row=7,column=2)
        self.gridx_ent.insert(0, "linspace(-4*tower_height,4*tower_height,10)")

        w = Label(self,text="South-north grid (m):")
        w.grid(row=8,column=1,sticky=W)
        self.gridy_ent = Entry(self,width=36)
        self.gridy_ent.grid(row=8,column=2)
        self.gridy_ent.insert(0, "linspace(-4*tower_height,4*tower_height,10)")

        self.compute_btn = Button(self, text="Start computation", width=15, command=self.compute_btn_handler)
        self.compute_btn.grid(row=9,column=1,pady=10,sticky=E)

        w = Label(self,text=" ",fg="red")
        w.grid(row=0,column=3,pady=10,sticky=W)

        self.periodicCall()

    def close_handler(self):
        self.cancel_event.set()
        self.master.quit()

    def parse_entries(self):
        self.phi = 0
        self.latitude = float(eval(self.lat_ent.get()))
        tower_height = float(eval(self.height_ent.get()))
        self.tower_height = tower_height
        self.tower_diameter = float(eval(self.diam_ent.get()))
        self.time_vector = eval(self.time_ent.get())
        x = eval(self.gridx_ent.get())
        y = eval(self.gridy_ent.get())
        X,Y = meshgrid(x,y)
        self.X = X
        self.Y = Y

    def compute_btn_handler(self):
        if self.computing:
            self.cancel_event.set()
            self.thread1.join()
            self.compute_btn.config(text="Start computation")
        else:
            self.cancel_event = threading.Event()
            self.meter = Meter(self, relief='ridge', bd=3, width=250)
            self.meter.grid(row=9,column=2)
            self.parse_entries()
            self.compute_btn.config(text="Stop computation")
            self.thread1 = threading.Thread(target=self.worker_thread)
            self.thread1.start()


    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        while self.progress_queue.qsize():
            try:
                msg = self.progress_queue.get(0)
                if msg == 1.0:
                    self.meter.set(msg,"Completed successfully")
                else:
                    self.meter.set(msg)
            except Queue.Empty:
                pass
        if self.computing:
            self.compute_btn.config(text="Stop computation")
        else:
            self.compute_btn.config(text="Start computation")

        if self.S != None:
            self.plot_shadow_map()
            self.S = None

        self.master.after(100, self.periodicCall)
    
    def plot_shadow_map(self):
        ion()
        contourf(self.X, self.Y, self.S/3600.,levels=[0.1,5,10,15,30,40,50,100,1e6],cmap=cm.get_cmap(name="gist_heat_r"))
        clim(0,100)
        colorbar()
        CS = contour(self.X, self.Y, self.S/3600.,levels=[0.0001,5,10,15,30,40,50,100],antialiased=True,colors='k')
        clabel(CS, inline=1, fontsize=8)
        xlabel('Location west-east (m)')
        ylabel('Location south-north (m)')
	show()

    def worker_thread(self):
        self.S = None
        self.computing = True
        S = shadow.tower_shadow_map(self.phi, \
                                    self.latitude*pi/180., \
                                    self.tower_height, \
                                    self.tower_diameter, \
                                    self.time_vector, \
                                    self.X, \
                                    self.Y, \
                                    self.progress_queue, \
                                    self.cancel_event)
        self.S = S

        self.computing = False

app = App()
app.master.title("Shadowtime")

app.mainloop()
