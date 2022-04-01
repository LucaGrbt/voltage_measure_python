# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:51:38 2022

@author: LucaGraebenteich
"""

import sys
import time
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from serial import Serial
import csv
# from gpiozero import MCP3008
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *

            
ser = Serial("COM3", 115200)
start_time = time.time()

class VoltagePlot(QtGui.QWidget):
    def __init__(self, parent=None):
        super(VoltagePlot, self).__init__(parent)

        self.setLayout(QtGui.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()             # create GrpahicsLayoutWidget obejct  
        self.layout().addWidget(self.canvas)

        self.label = QtGui.QLabel()                         # placeholder Qlabel object to display framerate
        self.layout().addWidget(self.label)

        #  Set up plot
        self.analogPlot = self.canvas.addPlot(title="Gemessener Output der Messbruecke")
        self.analogPlot.setYRange(0, 3)                # set y-axis range
        self.analogPlot.setXRange(0 , 600)             # set x-axis range
        self.analogPlot.showGrid(x=True, y=True, alpha=0.5)
        x_axis = self.analogPlot.getAxis('bottom')
        y_axis = self.analogPlot.getAxis('left')
        
        x_axis.setLabel(text='time [s]')              # set axis labels
        y_axis.setLabel(text='calculated analog voltage')

        xticks = [[(0,'0'),(600,'600')],[(60,'60'),(120,'120'),(180,'180'),(240,'240'),(300,'300'),(360,'360'),(420,'420'),(480,'480'),(540,'540')]]
        yticks = [[(0,'0'),(6,'6')],[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]]
        x_axis.setTicks(xticks)                              # set ticks manually (first major-ticks than minor-ticks)
        y_axis.setTicks(yticks)
        
        self.drawplot = self.analogPlot.plot(pen='y')       # yellow line plot

        # initialize sensor data variables
        self.numPoints = 10000                    # number of points that should be plottet at the same time stamp
        self.x = np.array([], dtype=float)        # create empty numpy array to store xAxis data
        self.y = np.array([], dtype=float)        # create empty numpy array to store yAxis data

        #initialize array for saving all measure data in csv-file
        self.save_time = np.array([], dtype=float)
        self.save_voltage = np.array([], dtype=float)

        # initialize frame counter variables 
        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        # set up image exporter (necessary to be able to export images)
        QtGui.QApplication.processEvents()
        self.exporter=pg.exporters.ImageExporter(self.canvas.scene())
        self.image_counter = 1

        # start updating
        self._update()
        
        # show plot
        self.show()

    def _framerate(self):
        now = time.time()   # current time since the epoch in seconds
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        self.label.setText(tx)
        QtCore.QTimer.singleShot(1, self._update)
        self.counter += 1

    def _save_image(self):
        filename = 'img'+("%04d" % self.image_counter)+'.png'
        self.exporter.export(filename)
        self.image_counter += 1

    def _update(self):     
###Getting data
        time.sleep(0.001)                                                 #determine measure frequency
        ser_bytes = ser.readline()
        ser_data = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        voltage = ser_data * 3.3 - 0.01                              #read the text line from serial port
        process_time = time.time() - start_time
        dataArray = (process_time, voltage)                       #split it into an array

###Passing data for plotting
        xAxis = float(dataArray[0])                                   #convert first element to an integer
        yAxis = float(dataArray[1])                            #convert and flip yAxis signal     

###Saving data for later csv transfer
        self.save_time = np.append(self.save_time, float(dataArray[0]))
        self.save_voltage = np.append(self.save_voltage, float(dataArray[1]))

###Plotting, no changes so far        
        self.x = np.append(self.x, xAxis)                           # append new data point to the array
        if self.x.size >= self.numPoints:                           # make sure that the size of the array includes the most recent data points
            self.x = np.append(self.x[1:self.numPoints],xAxis)
        else:
            self.x = np.append(self.x,xAxis) 

        self.y = np.append(self.y, yAxis)                           # append new data point to the array
        if self.y.size >= self.numPoints:                           # make sure that the size of the array includes the most recent data points
            self.y = np.append(self.y[1:self.numPoints],yAxis)
        else:
            self.y = np.append(self.y,yAxis)

        self.drawplot.setData(self.x, self.y)                       # draw current data set
        
        self._framerate()                                           # update framerate, see corresponding function

        # self._save_image()    # uncomment this to save each frame as an .png image in your current directory. Note that the framerate drops significantly by doing so    

if __name__ == '__main__':
    
    
    app = QtGui.QApplication(sys.argv)
    ex = VoltagePlot()
    ex.show()
    sys.exit(app.exec_())