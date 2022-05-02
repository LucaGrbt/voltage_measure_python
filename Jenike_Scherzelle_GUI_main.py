# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:52:15 2022

@author: LucaGraebenteich
"""

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Jenike_Scherzelle_GUIraw3.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

"""
Don't change this file, unless you know exactly what you're doing
Create all the functionalities in the main.py
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import VoltagePlot form real_time_plot and embed it as widget in the Main GUI
from real_time_plot_widget import VoltagePlot

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName(u"Messprogramm Jenike-Scherzelle")
        MainWindow.resize(1024, 730)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        # show progress of shear distance according to measurement time and maximum shear distance
        self.progressed_shear_distance = QProgressBar(self.centralwidget)
        self.progressed_shear_distance.setObjectName(u"progressed_shear_distance")
        self.progressed_shear_distance.setGeometry(QRect(10, 640, 1004, 23))
        # self.progressed_shear_distance.setValue(0)
        # start live plot and recording data
        self.start_measure = QPushButton(self.centralwidget)
        self.start_measure.setObjectName(u"start_measure")
        self.start_measure.setGeometry(QRect(10, 110, 180, 24))
        # decide if live plot shall be shown or not
        # self.live_plot_activation = QCheckBox(self.centralwidget)
        # self.live_plot_activation.setObjectName(u"live_plot_activation")
        # self.live_plot_activation.setGeometry(QRect(10, 150, 151, 20))
        # pause live plot and recording data
        self.pause_measure = QPushButton(self.centralwidget)
        self.pause_measure.setObjectName(u"pause_measure")
        self.pause_measure.setGeometry(QRect(10, 230, 180, 24))
        # continue live plot and recording data
        self.continue_measure = QPushButton(self.centralwidget)
        self.continue_measure.setObjectName(u"continue_measure")
        self.continue_measure.setGeometry(QRect(10, 260, 180, 24))
        # show current date and time
        self.date_time = QLabel(self.centralwidget)
        self.date_time.setObjectName(u"date_time")
        self.date_time.setGeometry(QRect(900, 0, 161, 20))
        # show current voltage
        self.current_voltage_info = QLabel(self.centralwidget)
        self.current_voltage_info.setObjectName(u"date_time")
        self.current_voltage_info.setGeometry(QRect(10, 140, 180, 24))
        self.current_voltage_info.setAlignment(Qt.AlignCenter)
        self.current_voltage = QLabel(self.centralwidget)
        self.current_voltage.setObjectName(u"date_time")
        self.current_voltage.setGeometry(QRect(10, 170, 180, 24))
        self.current_voltage.setAlignment(Qt.AlignCenter)
        # end measurement and stop recording data
        self.end_measure = QPushButton(self.centralwidget)
        self.end_measure.setObjectName(u"end_measure")
        self.end_measure.setGeometry(QRect(10, 350, 180, 24))
        # save recorded data as .csv and .xlsx file
        self.save_values_xlsx = QPushButton(self.centralwidget)
        self.save_values_xlsx.setObjectName(u"save_values_xlsx")
        self.save_values_xlsx.setGeometry(QRect(10, 440, 180, 24))
        # self.save_values_csv = QPushButton(self.centralwidget)
        # self.save_values_csv.setObjectName(u"save_values_csv")
        # self.save_values_csv.setGeometry(QRect(10, 470, 151, 24))
        # open calibration window
        self.start_calibration = QPushButton(self.centralwidget)
        self.start_calibration.setObjectName(u"start_calibration")
        self.start_calibration.setGeometry(QRect(10, 20, 180, 24))   
        # show live data
        self.voltage_plot = VoltagePlot(self.centralwidget)
        self.voltage_plot.setObjectName(u"VoltagePlot")
        self.voltage_plot.setGeometry(QRect(190, 22, 800, 600))
        # type in students group, number etc.
        self.students_data = QLineEdit(self.centralwidget)
        self.students_data.setObjectName(u"students_data")
        self.students_data.setGeometry(QRect(10, 675, 1004, 23))
        font1 = QFont()
        font1.setPointSize(12)
        # main window general stuff
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.date_time.setBuddy(self.date_time)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Messprogramm Jenike-Scherzelle", None))
        self.start_measure.setText(QCoreApplication.translate("MainWindow", u"Messung starten", None))
        self.current_voltage_info.setText(QCoreApplication.translate("MainWindow", u"Aktuelle Spannung [V]:", None))
        # self.live_plot_activation.setText(QCoreApplication.translate("MainWindow", u"Plot aktivieren", None))
        self.pause_measure.setText(QCoreApplication.translate("MainWindow", u"Messung anhalten", None))
        self.continue_measure.setText(QCoreApplication.translate("MainWindow", u"Messung fortsetzen", None))
        self.date_time.setText(QCoreApplication.translate("MainWindow", u"Hier Datum,... Zeit", None))
        self.end_measure.setText(QCoreApplication.translate("MainWindow", u"Messung abgeschlossen", None))
        self.save_values_xlsx.setText(QCoreApplication.translate("MainWindow", u"Werte speichern (.xlsx)", None))
        # self.save_values_csv.setText(QCoreApplication.translate("MainWindow", u"Werte speichern (.csv)", None))
        self.start_calibration.setText(QCoreApplication.translate("MainWindow", u"Eichung durchf\u00fchren", None))
        self.students_data.setText(QCoreApplication.translate("MainWindow", u"Hier Gruppe/Namen eingeben zum Speichern der Daten", None))
    # retranslateUi
