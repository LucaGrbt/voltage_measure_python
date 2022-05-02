# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:51:38 2022

Source code from JaFeKl/joystick_real_time_plot_with_pyqtgraph

https://github.com/JaFeKl/joystick_real_time_plot_with_pyqtgraph

@author: LucaGraebenteich
"""

import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
# from serial import Serial
from gpiozero import MCP3008
import csv
import queue



class VoltagePlot(QWidget):
    
    
    def __init__(self, parent=None):
        super(VoltagePlot, self).__init__(parent)
        
        self.setLayout(QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()                         # create GrpahicsLayoutWidget obejct  
        self.layout().addWidget(self.canvas)

        self.label = QLabel()                                           # placeholder Qlabel object to display framerate
        self.layout().addWidget(self.label)

        #  Set up plot
        self.analogPlot = self.canvas.addPlot(title="Gemessener Output der Messbruecke")
        self.analogPlot.setYRange(0, 1)                # set y-axis range
        self.analogPlot.setXRange(0 , 60)             # set x-axis range
        self.analogPlot.showGrid(x=True, y=True, alpha=0.5)
        self.x_axis = self.analogPlot.getAxis('bottom')
        self.y_axis = self.analogPlot.getAxis('left')
        
        self.x_axis.setLabel(text='time [s]')              # set axis labels
        self.y_axis.setLabel(text='calculated analog voltage')

        self.minute_counter = 0
        self.xticks = [[(0,'0'),(60,'60')],[]]                          # x ticks are automatically extended by main_Messprogramm, update_voltage_plot function
        self.yticks = [[(0,'0'),(1,'1')],[(0.1,'0.1'),(0.2,'0.2'),(0.3,'0.3'),(0.4,'0.4'),(0.5,'0.5'),(0.6,'0.6'),(0.7,'0.7'),(0.8,'0.8'),(0.9,'0.9')]]        
        # xticks = [[(0,'0'),(600,'600')],[(60,'60'),(120,'120'),(180,'180'),(240,'240'),(300,'300'),(360,'360'),(420,'420'),(480,'480'),(540,'540')]]  # set ticks manually (first major-ticks than minor-ticks)
        # yticks = [[(0,'0'),(6,'6')],[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]]
        self.x_axis.setTicks(self.xticks)                               
        self.y_axis.setTicks(self.yticks)
        
        self.drawplot = self.analogPlot.plot(pen='y')                   # yellow line plot

        # initialize sensor data variables
        self.numPoints = 10000                                          # number of points that should be plottet at the same time stamp
        self.x = np.array([], dtype=float)                              # create empty numpy array to store xAxis data
        self.y = np.array([], dtype=float)                              # create empty numpy array to store yAxis data

        #initialize array for saving all measure data in csv-file
        # self.save_time = np.array([], dtype=float)
        # self.save_voltage = np.array([], dtype=float)
        self.save_time = []
        self.save_voltage = []

        # initialize frame counter variables 
        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        # set up image exporter (necessary to be able to export images)
        QApplication.processEvents()
        self.exporter=pg.exporters.ImageExporter(self.canvas.scene())
        self.image_counter = 1
    
        self.plot_data = queue.Queue(maxsize = 100)
        
        # # start updating
        # self._update()
        
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
        QTimer.singleShot(1, self._update)
        self.counter += 1

    def _save_image(self):
        filename = 'img'+("%04d" % self.image_counter)+'.png'
        self.exporter.export(filename)
        self.image_counter += 1

    def _update(self):
        if self.plot_data.empty():
            pass
        else:
###Getting data
            # global start_time
            # time.sleep(0.0009)                                          #determine measure frequency
            # ser_bytes = ser.readline()
            # ser_data = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            plot_data  = self.plot_data.get()
            voltage = plot_data[0]                                      #read the text line from serial port
            process_time = plot_data[1]
            # process_time = time.time() - start_time
            dataArray = (process_time, voltage)                         # split it into an array
    
    ###Passing data for plotting
            xAxis = float(dataArray[0])                                 
            yAxis = float(dataArray[1])                                     
    
    ###Saving data for later csv transfer
            # self.save_time = np.append(self.save_time, float(dataArray[0]))
            # self.save_voltage = np.append(self.save_voltage, float(dataArray[1]))
            self.save_time.append(dataArray[0])
            self.save_voltage.append(dataArray[1])
    
    ###Plotting, no changes so far        
            self.x = np.append(self.x, xAxis)                           # append new data point to the array
            if self.x.size >= self.numPoints:                           # make sure that the size of the array includes the most recent data points
                self.x = np.append(self.x[0:self.numPoints:2],xAxis)    # plot whole process time, while lowering resolution with growing process time
                # self.x = np.append(self.x[1:self.numPoints],xAxis)    # plot numPoints with same resolution but limited plottable process time(last measure points will continuously be deleted after reaching number of numPoints
            else:
                self.x = np.append(self.x,xAxis) 
    
            self.y = np.append(self.y, yAxis)                           # append new data point to the array
            if self.y.size >= self.numPoints:                           # make sure that the size of the array includes the most recent data points
                self.y = np.append(self.y[0:self.numPoints:2],yAxis)
                # self.y = np.append(self.y[1:self.numPoints],yAxis)
            else:
                self.y = np.append(self.y,yAxis)
    
            self.drawplot.setData(self.x, self.y)                       # draw current data set
            
            self._framerate()                                           # update framerate, see corresponding function
    
            # self._save_image()                                        # uncomment this to save each frame as an .png image in your current directory. Note that the framerate drops significantly by doing so    

if __name__ == '__main__':
    ser = Serial("COM3", 115200)
    start_time = time.time()
    app = QApplication(sys.argv)
    ex = VoltagePlot()
    ex.show()
    sys.exit(app.exec_())
