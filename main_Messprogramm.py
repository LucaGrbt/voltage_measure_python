# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:43 2022

@author: LucaGraebenteich
"""
# import standard pyqt modules
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import other necessary modules
import time
import time as mt   # import module for voltage data plot thread
import time as pt   # import module for progress bar thread 
import time as ct   # import module for calibration thread
import time as tt   # import module for trigger thread
import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
# from serial import Serial
from gpiozero import MCP3008
import RPi.GPIO as GPIO
import xlsxwriter
from datetime import datetime
import matplotlib.pyplot as plt

# import Main GUI + additional GUIs
from Jenike_Scherzelle_GUI_main import Ui_MainWindow
from Jenike_Scherzelle_GUI_Eichung import Ui_Calibration_Window
from Jenike_Scherzelle_GUI_SpeicherWarnung import Ui_Save_Error_Window

# set the time variables as global variables as there are multiple classes that have to get them
process_time_run = 0
process_time_pause = 0

# import GUIs and set up functionalities for Main GUI
class Messprogramm(QMainWindow, Ui_MainWindow):                         # put in Ui_MainWindow that was converted by uic to setupUi later
    def __init__(self, parent=None):
        super(Messprogramm, self).__init__(parent)
        self.setupUi(self)                                              # set up Ui_MainWindow
        
        ### first set up additional Widgets/Windows
        # calibration window running in background
        self.calibration_window = QWidget()
        self.calibration_ui = Ui_Calibration_Window()
        self.calibration_ui.setupUi(self.calibration_window)
        
        ### set up button functionalities
        
        ### calibration functionalities
        # open calibration window by button
        self.start_calibration.clicked.connect(lambda: self.open_calibration_window())
        # create list to save calibration data by click
        self.calibration_data = []
        # connect buttons of calibration window
        self.calibration_ui.append_weight_voltage_pair.clicked.connect(lambda: self.append_calibration_data())
        self.calibration_ui.plot_calibration_curve.clicked.connect(lambda: self.save_calibration_data())
        self.calibration_ui.delete_last_calibration_data.clicked.connect(lambda: self.delete_calibration_data())
        
        ### plotting and prgress bar functions
        # functions for start button
        self.start_measure.clicked.connect(lambda: self.start_functions())      # difficutlies appeared when connecting two functions to on button directly, so there was one function connected to the button which later calls both wanted functions
        self.start_measure.setEnabled(True)
        # functions for pause button
        self.pause_measure.clicked.connect(lambda: self.stop_functions())
        self.pause_measure.setEnabled(False)
        # functions for continue button
        self.continue_measure.clicked.connect(lambda: self.continue_functions())
        self.continue_measure.setEnabled(False)
        # functions for end button
        self.end_measure.clicked.connect(lambda: self.end_functions())
        self.end_measure.setEnabled(False)
        
        ### saving functions
        # functions for save csv button
        # self.save_values_csv.clicked.connect(lambda: self.save_csv())
        # self.save_values_csv.setEnabled(False)
        # functions for save xlsx button
        self.save_values_xlsx.clicked.connect(lambda: self.save_xlsx())
        self.save_values_xlsx.setEnabled(False)
        
        # get max shear time/distance from laboratory experimentally for progress bar
        self.max_shear_time = 120 # seconds
        
        # initialize thread dictionary to set up threads later (NECESSARY!)
        self.thread={}
        
        # get current date for the right corner QLabel of the window
        self.date_time.setText(self.get_date())
        
        # initialize DutyCycle of servo motor for the laboratory test rig without any status here (value = 0), work on it later in the switch functions, DutyCycles: 2.5 = 0 deg, 12.5 = 180 deg
        self.cycle = 0
        self.trigger_hold = 0                                           # define a time for how long to eletrically hold the servo switch by the PWM pulse later (servo has to be put off after switching by DutyCycle(0) to prevent if from shivering further on
        


    # get current date and time    
    def get_datetime(self):                 # get dat AND time
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d_%H-%M")
        # print(dt_string)
        return dt_string
    def get_date(self):                     # only get date
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        # print(dt_string)
        return dt_string
    
    
    ### button functionalities for calibration window
    # show calibration window from button    
    def open_calibration_window(self):
        self.trigger_testrig_on()                                       # put laboratory test rig on
        self.calibration_window.show()
        #self.calibration_window.show()
        self.thread[3] = ThreadClassCalibration(parent=None,index=3)
        self.thread[3].start()
        self.thread[3].calibration_signal.connect(self.display_calibration_voltage)
        self.pause_measure.setEnabled(False)
        self.continue_measure.setEnabled(False)
        self.end_measure.setEnabled(False)
        self.save_values_xlsx.setEnabled(False)
    
    # show current voltage in calibration window by thread 3
    def display_calibration_voltage(self, ser_data):
        self.calibration_ui.current_measure_display.setText(str(ser_data))
        
    # append weight/voltage pair to calibration data
    def append_calibration_data(self):
        self.calibration_data.append([float(self.calibration_ui.current_weight_input.text()), float(self.calibration_ui.current_measure_display.text())])
        print(self.calibration_data)
    
    # save calibration data as Excel and export plot as pdf
    def save_calibration_data(self):
        if self.students_data.text() == "Hier Gruppe/Namen eingeben zum Speichern der Daten" or "/" in self.students_data.text() or ":" in self.students_data.text():
            self.open_save_error_window()
        else:   
            # save data in Excel file 
            file = xlsxwriter.Workbook("/home/pi/Desktop/SA_MVT_Jenike/MessDaten_Plots/Jenike_Messdaten-EICHKURVE-"+str(self.students_data.text())+"-"+str(self.get_datetime())+".xlsx")
            table = file.add_worksheet()
            # table.writer(0, 0, "Versuch Jenike Scherzelle"+str(lineEdit Eingabefeld)+str(Datum))                   ### hier noch Datum einfügen + lineedit für Gruppenname
            table.write(0, 0, "Jenike_Messdaten-EICHKURVE-"+str(self.students_data.text())+"-"+str(self.get_datetime()))
            table.write(1, 0, "Gewicht [kg]")
            table.write(1, 1, "Spannung [V]")
            for i in range(len(self.calibration_data)):
                table.write(i+2, 0, self.calibration_data[i][0])
                table.write(i+2, 1, self.calibration_data[i][1])
            file.close()
            # Plot data and save as pdf
            x = []
            y = []
            for i in range(len(self.calibration_data)):
                x.append(self.calibration_data[i][0])
                y.append(self.calibration_data[i][1])
            plt.plot(x, y, 'b+')
            plt.xlabel("Gewicht [kg]")
            plt.ylabel("Spannung [V]")
            plt.title("Eichkurve Jenike Scherzelle_"+self.get_datetime())
            plt.axis([0, 6, 0, 2])
            plt.grid(True)
            plt.savefig("/home/pi/Desktop/SA_MVT_Jenike/MessDaten_Plots/Jenike_Messdaten-EICHKURVE-Plot-"+str(self.students_data.text())+"-"+str(self.get_datetime())+".pdf")
            plt.show()
            # stop calibration window thread
            self.thread[3].terminate()                                  # close thread [3] because should only be one thread allowed to wrap analog data from GPIO pin
            # self.start_measure.setEnabled(True)
     
    # delete calibration data for new calibration curve
    def delete_calibration_data(self):
        self.calibration_data = []
        print(self.calibration_data)


    ### call multiple button functions that run on seperate threads, voltage plot on thread[1], progress bar on thread[2], laboratory test rig trigger on thread[4] 
    def start_functions(self):
        self.start_voltage_plot()                                       # start plotting voltage over time
        self.start_progress_bar()                                       # start progress bar
        self.trigger_testrig_on()                                       # put laboratory test rig on, get the currect DutyCycle (2.5 = 0 deg, 12.5 = 180 deg) for on/off status of the GPIO Analog Zero servo motor by testing on the swtich of the test rig
        
        
    def stop_functions(self):
        self.stop_voltage_plot()                                        # the following are mostly similar functions for starting/stoptting/ending measuring, progress bar, trigger
        self.stop_progress_bar()                                        # please watch the detailed functionalities in the following functions
        self.trigger_testrig_off()
        
    def continue_functions(self):
        self.continue_voltage_plot()
        self.continue_progress_bar()
        self.trigger_testrig_on()
        
    def end_functions(self):
        self.end_measurement()
        self.end_progress_bar()
        self.trigger_testrig_off()
        
    ### button functionalities for voltage plotting on thread[1]
    def start_voltage_plot(self):
        if 3 in self.thread:                                            # check if thread is currently in thread dictionary of GUI
            if self.thread[3].is_running == True:                       # check if thread is running
                self.thread[3].terminate()                              # close thread [3] because there should only be one thread allowed to wrap analog data from GPIO pin
        global process_time_pause
        global process_time_run
        process_time_run = 0
        process_time_pause = time.time()
        self.voltage_plot.x = np.array([], dtype=float)                 # create empty numpy array to store xAxis data
        self.voltage_plot.y = np.array([], dtype=float)                 # create empty numpy array to store yAxis data
        self.voltage_plot.save_time = []
        self.voltage_plot.save_voltage = []
        self.voltage_plot.minute_counter = 0
        self.thread[1] = ThreadClassPlot(parent=None,index=1)
        self.thread[1].start()
        self.thread[1].plot_data.connect(self.update_voltage_plot)
        
        # change buttons
        self.start_calibration.setEnabled(False)
        self.start_measure.setEnabled(False)
        self.pause_measure.setEnabled(True)
        self.continue_measure.setEnabled(False)
        self.end_measure.setEnabled(True)
        self.save_values_xlsx.setEnabled(False)
        # self.save_values_csv.setEnabled(False)
        
    def stop_voltage_plot(self):
        self.thread[1].stop()
        self.pause_measure.setEnabled(False)
        self.continue_measure.setEnabled(True)
        self.end_measure.setEnabled(True)
        
    def continue_voltage_plot(self):
        global process_time_pause
        process_time_pause = time.time()
        self.thread[1] = ThreadClassPlot(parent=None,index=1)
        self.thread[1].start()
        self.thread[1].plot_data.connect(self.update_voltage_plot)
        self.pause_measure.setEnabled(True)
        self.continue_measure.setEnabled(False)
        self.end_measure.setEnabled(True)
        self.start_calibration.setEnabled(False)
        self.save_values_xlsx.setEnabled(False)
        
    def end_measurement(self):
        self.thread[1].stop()
        self.start_measure.setEnabled(True)
        self.pause_measure.setEnabled(False)
        self.continue_measure.setEnabled(True)
        self.end_measure.setEnabled(False)
        # self.save_values_csv.setEnabled(True)
        self.save_values_xlsx.setEnabled(True)
        self.start_calibration.setEnabled(True)
        
    # update function for voltage plot
    def update_voltage_plot(self, ser_data, process_time):
        # self.calibration_ui.current_measure_display.setText(str(ser_data))
        self.current_voltage.setText(str(ser_data))
        # update plot grid xAxis/time with every minute
        if process_time >= self.voltage_plot.minute_counter*60:
            self.voltage_plot.minute_counter += 1                       
            self.voltage_plot.analogPlot.setXRange(0 , self.voltage_plot.minute_counter*60)             # set x-axis range
            self.voltage_plot.analogPlot.showGrid(x=True, y=True, alpha=0.5)
            self.voltage_plot.xticks[0][1] = (self.voltage_plot.minute_counter*60, str(self.voltage_plot.minute_counter*60))
            if self.voltage_plot.minute_counter >= 2:
                self.voltage_plot.xticks[1].append(((self.voltage_plot.minute_counter-1)*60, str((self.voltage_plot.minute_counter-1)*60)))
                self.voltage_plot.x_axis.setTicks(self.voltage_plot.xticks)
        # update voltage data as long as there is free place in the queue (plot_data) of voltage plot und update plot (graphically) with ._update() function
        if self.voltage_plot.plot_data.full():
            pass
        else:
            self.voltage_plot.plot_data.put([ser_data, process_time])
            self.voltage_plot._update()
            
    ### button functionalities for progress bar (shear distance) on thread[2]     
    def start_progress_bar(self):
        self.thread[2] = ThreadClassProgress(parent=None,index=2)
        self.thread[2].start()
        self.thread[2].shear_info.connect(self.update_progress_bar)
        
    def stop_progress_bar(self):
        self.thread[2].stop()
        
    def continue_progress_bar(self):
        self.thread[2] = ThreadClassProgress(parent=None,index=2)
        self.thread[2].start()
        self.thread[2].shear_info.connect(self.update_progress_bar)
        
    def end_progress_bar(self):
        self.thread[2].stop()
    
    # update function for progress bar
    def update_progress_bar(self, process_time):
        progressed_shear = process_time/self.max_shear_time*100         # progressed shear distance in percent
        self.progressed_shear_distance.setValue(int(progressed_shear))
    
    
    ### button functionalities for test rig trigger on thread [4]
    # switch test rig "on"
    def trigger_testrig_on(self):
        #if 4 in self.thread:
           # if self.thread[4].is_running == True:
               # print('Thread 4 closed')
               # self.thread[4].terminate()
        print(self.cycle)
        self.trigger_hold = time.time()
        self.thread[4] = ThreadClassTrigger(parent=None,index=4)
        self.thread[4].start()
        self.thread[4].trigger_signal.connect(self.switch_testrig_on)
    
    # switch function connected to trigger thread[4]    
    def switch_testrig_on(self):
        if self.cycle != 6.0:
            self.cycle = 6.0
            print('trigger function started by signal')
            servm.start(self.cycle) # Initialization
            #time.sleep(0.1)
            servm.ChangeDutyCycle(self.cycle)        
        elif time.time()-self.trigger_hold >= 1: 
            servm.ChangeDutyCycle(0) 
            self.trigger_hold = 0                                  # DutyCycles: 2.5 = 0 deg, 12.5 = 180 deg
            self.thread[4].stop()
    
    # switch test rig "off"
    def trigger_testrig_off(self):
        #if 4 in self.thread:
         #   if self.thread[4].is_running == True:
          #      print('Thread 4 closed')
           #     self.thread[4].terminate()
        print(self.cycle)
        self.trigger_hold = time.time()
        self.thread[4] = ThreadClassTrigger(parent=None,index=4)
        self.thread[4].start()
        print('Thread 4 started')
        self.thread[4].trigger_signal.connect(self.switch_testrig_off)
    
    # switch function connected to trigger thread[4]    
    def switch_testrig_off(self):
        if self.cycle != 8.5:
            self.cycle = 8.5
            print('trigger function started by signal')
            servm.start(self.cycle) # Initialization
            servm.ChangeDutyCycle(self.cycle)  
        elif time.time()-self.trigger_hold >= 1:          
            servm.ChangeDutyCycle(0)
            self.trigger_hold = 0
            self.thread[4].stop()                                   # DutyCycles: 2.5 = 0 deg, 12.5 = 180 deg
        
    ### button functionalities for saving data and plots
    # def save_csv(self):
    #     data_time = self.voltage_plot.save_time
    #     data_voltage = self.voltage_plot.save_voltage
    #     with open('jenike_messdaten.csv', 'w', newline='\n') as csvfile:
    #         datawriter = csv.writer(csvfile)
    #         for i in range(len(data_time)):
    #             datawriter.writerow(str(data_time)+","+str(data_voltage))
    
    # saving data as Excel file and save plot as pdf
    def save_xlsx(self):
        if self.students_data.text() == "Hier Gruppe/Namen eingeben zum Speichern der Daten" or "/" in self.students_data.text() or ":" in self.students_data.text():
            self.open_save_error_window()
        else:
            # save data in Excel file 
            data_time = self.voltage_plot.save_time
            data_voltage = self.voltage_plot.save_voltage
            file = xlsxwriter.Workbook("/home/pi/Desktop/SA_MVT_Jenike/MessDaten_Plots/Jenike_Messdaten-SCHERZELLE"+str(self.students_data.text())+"-"+str(self.get_datetime())+".xlsx")
            table = file.add_worksheet()
            # table.writer(0, 0, "Versuch Jenike Scherzelle"+str(lineEdit Eingabefeld)+str(Datum)) 
            table.write(0, 0, "Jenike_Messdaten-SCHERZELLE-"+str(self.students_data.text())+"-"+str(self.get_datetime()))
            table.write(1, 0, "Zeit [s]")
            table.write(1, 1, "Spannung [V]")
            for i in range(len(data_time)):
                table.write(i+2, 0, data_time[i])
                table.write(i+2, 1, data_voltage[i])
            file.close()
            # plot data and save as pdf
            x = []
            y = []
            for i in range(len(data_time)):
                x.append(data_time[i])
                y.append(data_voltage[i])
            plt.plot(x, y, 'b,')
            plt.xlabel("Zeit [s]")
            plt.ylabel("Spannung [V]")
            plt.title("Spannung Jenike Scherzelle_"+self.get_datetime())
            # plt.axis([0, 180, 0, 5])
            plt.grid(True)
            plt.savefig("/home/pi/Desktop/SA_MVT_Jenike/MessDaten_Plots/Jenike_Messdaten-SCHERZELLE-Plot-"+str(self.students_data.text())+"-"+str(self.get_datetime())+".pdf")
            plt.show()
    
    # popping error message when there is no group name typed in     
    def open_save_error_window(self):
        self.save_error_window = QWidget()
        self.save_error_ui = Ui_Save_Error_Window()
        self.save_error_ui.setupUi(self.save_error_window)
        self.save_error_window.show()
        

### Multithreading for responsive GUI
# thread class for voltage plot in widget
class ThreadClassPlot(QThread):
    plot_data = pyqtSignal(float, float)                                # send signal with two float type data
    def __init__(self, parent=None,index=0):
        super(ThreadClassPlot, self).__init__(parent)
        self.index=index
        self.is_running = True    
    def run(self):                                                      # run(self) function will be called as the thread is started by button
        global process_time_run
        global process_time_pause
        while (True):
            # manipulate measurement frequency
            mt.sleep(0.009) 
            self.process_time = mt.time() - process_time_pause + process_time_run
                
            # use "serial" module for arduino data
            # ser_bytes = ser.readline()
            # ser_data = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            
            # use "gpiozero" module for raspberry pi data with MCP3008
            voltage = adc.value
            ser_data = voltage * 3.3 - 0.0098                           # gpio emits signals from 0 (0V) to 1 (3.3V) - formula necessary to get correct voltage including other electric impacts from crowbar and RaspberryPi4 (Klemmschaltung/Ueberspannungsschutz)etc.
            ser_data = float('{:.4f}'.format(ser_data))                 # format float value to 4 decimals
            self.plot_data.emit(ser_data, self.process_time)            # voltage plot needs both, current voltage and time data, both in float format
            self.last_point = mt.time()
            
    def stop(self):
        global process_time_run
        process_time_run = self.process_time
        self.is_running = False
        self.terminate()

# thread class for progress bar
class ThreadClassProgress(QThread):
    shear_info = pyqtSignal(float)
    def __init__(self, parent=None,index=0):
        super(ThreadClassProgress, self).__init__(parent)
        self.index=index
        self.is_running = True    
    def run(self):                                                      # run(self) function will be called as the thread is started by button
        global process_time_run
        global process_time_pause
        while (True):
            pt.sleep(0.1)                                             # manipulate measurement frequency
            self.process_time = time.time() - process_time_pause + process_time_run
            self.shear_info.emit(self.process_time)                     # progress bar only needs time, no matter if int, or float format (time naturally given in float)
    
    def stop(self):
        self.is_running = False
        self.terminate()
    
# thread class for calibration window widget
class ThreadClassCalibration(QThread):
    calibration_signal = pyqtSignal(float)
    def __init__(self, parent=None,index=0):
        super(ThreadClassCalibration, self).__init__(parent)
        self.index=index
        self.is_running = True    
    def run(self):                                                      # run(self) function will be called as the thread is started by button
        while (True):
            ct.sleep(0.01)                                            # manipulate measurement frequency
            
            # use arduino controller for data                                  
            # ser_bytes = ser.readline()
            # ser_data = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            
            # use gpiozero for raspberry pi data with MCP3008
            voltage = adc.value
            ser_data = voltage * 3.3 - 0.1                              # gpio emits signals from 0 (0V) to 1 (3.3V) - formula necessary to get correct voltage including other electric impacts from crowbar (Klemmschaltung/Ueberspannungsschutz)etc.
            ser_data = float('{:.4f}'.format(ser_data))
            
            self.calibration_signal.emit(ser_data)                      # calibration window only needs the current voltage in float format
           
    def stop(self):
        self.is_running = False
        self.terminate()      

# thread class for trigger of measured test rig
class ThreadClassTrigger(QThread):
    trigger_signal = pyqtSignal()
    def __init__(self, parent=None,index=0):
        super(ThreadClassTrigger, self).__init__(parent)
        self.index=index
        self.is_running = True      
    def run(self):                                                      # run(self) function will be called as the thread is started by button
        while (True):
            tt.sleep(0.01)
            self.trigger_signal.emit()                                  # no values in signal, only give a signal to start triggering outside of main GUI loop
            
        
    def stop(self):
        print('Thread 4 terminated')
        self.is_running = False
        self.terminate()      

    
if __name__ == '__main__':        
    
    # set up voltage source (GPIO, RasperryPi own source), Arduino also possible
    # ser = Serial("COM3", 115200)                                      # serial for Arduino data reading
    adc = MCP3008(channel=7, device=0)                                  # gpio for Raspberry Pi data reading with MCP3008
    
    # set up servo motor for testrig switch
    servoPIN = 19                                                       # PIN on RaspioAnalogZero the servo motor is connected to
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    servm = GPIO.PWM(servoPIN, 50)                                     # GPIO 19 for PWM with 50Hz
    
    # get start_time of programm for later time calculations
    start_time = time.time()
    
    # start GUI/app/program
    app = QApplication([])
    messprogramm = Messprogramm()
    messprogramm.show()
    app.exec()
    
    
    
    
    
