#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Dan Bodoh
# Released under GPLv3

import tkinter as tk
from math import floor
import time
from pyacaia import AcaiaScale,find_acaia_devices,root
from engineering_notation import EngNumber
import tk_tools

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.createWidgets()
        self.scale = None
        self.weights = []
        self.times = []
        self.bind('<Destroy>',self.disconnectScale)
        self.mac=None

    def createWidgets(self):
        self.timeLabel = tk.Label(self,text='0:00',
                                        font='Helvetica 54')
        self.timeLabel.grid(column=0,row=0)
        self.weightLabel = tk.Label(self,text='0 g',
                                        font='Helvetica 54')
        self.weightLabel.grid(column=0,row=1)
        self.flowRateGauge = FlowRateGauge(self)
        self.flowRateGauge.grid(column=0,row=2)
        self.batteryLabel = tk.Label(self,text='Unconnected');
        self.batteryLabel.grid(column=0,row=3)

    def updateScale(self):
        if not self.mac:
            print("finding devices")
            addresses = find_acaia_devices()
            if addresses:
                self.mac = addresses[0]
                self.after(0,self.updateScale)
            else:
                self.after(5000,self.updateScale)
        elif not (self.scale and self.scale.connected):
            self.batteryLabel.config(text='Unconnected')
            print("connecting to scale")
            try:
                self.scale = AcaiaScale(self.mac)
                self.scale.connect()
            except Exception as e:
                print(str(e))
                pass
            self.after(1000,self.updateScale)
        else:
            self.weights.append(self.scale.weight)
            now = time.time()
            self.times.append(now)
            # average over 1.5 sec of data
            self.times[:] = filter(lambda t: now-t<=1.5, self.times)
            self.weights = self.weights[-len(self.times):]
            flowrate = 0
            if len(self.times)>1:
                flowrates = []
                for i in range(len(self.times)-1):
                    flowrates.append((self.weights[i+1]-self.weights[i])/
                                     (self.times[i+1]-self.times[i]))
                flowrate = sum(flowrates)/len(flowrates)
            weight_units = 'g'
            if self.scale.units=='grams':
                self.flowRateGauge.set_grams()
                self.weightLabel.config(
                    text=("%3.1f g" % self.scale.weight))
            elif self.scale.units=='ounces':
                self.flowRateGauge.set_ounces()
                self.weightLabel.config(
                    text=("%3.2f oz" % self.scale.weight))
            self.flowRateGauge.set_value(flowrate)
            elapsed = self.scale.get_elapsed_time()
            minutes = floor(elapsed / 60)
            seconds = floor( elapsed- (minutes*60 ))
            if seconds<10:
                seconds = '0'+str(seconds)
            self.timeLabel.config(text=(str(minutes)+':'+str(seconds)))
            self.batteryLabel.config(text=('Battery: '+str(self.scale.battery)+'%'))
            self.after(100,self.updateScale)

    def disconnectScale(*args):
        self = args[0]
        if self.scale and self.scale.connected:
            self.scale.disconnect()

class FlowRateGauge(tk_tools.Gauge):

    def __init__(self,parent):
        super().__init__(parent,
                              min_value=0,
                              max_value=3,
                              divisions=6,
                              label="Flow Rate",
                              unit="g/s",
                              width=300,
                              height=200,
                              yellow=0,
                              red=100)

    def set_grams(self):
        self._max_value = 3
        self._average_value = 1.5
        self._unit = 'g/s'


    def set_ounces(self):
        self._max_value = 0.1
        self._average_value = 0.05
        self._unit = 'oz/s'

    def set_value(self, value):
        self._value = EngNumber(value)
        if self._min_value * 1.02 < value < self._max_value * 0.98:
            self._redraw()
        else:
            self.readout(self._value,'black')

#root.setLevel(logging.DEBUG)
app = Application()
app.master.title('Flow Rate')
app.after(1000,app.updateScale)
app.mainloop()

