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

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QFont, QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

from real_time_plot_arduino_widget import VoltagePlot

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"Messprogramm Jenike-Scherzelle")
        MainWindow.resize(800, 600)
        # every GUI/MainWindow has to have a centralwidget - in this case place holder
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.progressed_shear_distance = QProgressBar(self.centralwidget)
        self.progressed_shear_distance.setObjectName(u"progressed_shear_distance")
        self.progressed_shear_distance.setGeometry(QRect(37, 520, 731, 23))
        self.progressed_shear_distance.setValue(24)
        self.start_measure = QPushButton(self.centralwidget)
        self.start_measure.setObjectName(u"start_measure")
        self.start_measure.setGeometry(QRect(10, 110, 151, 24))
        self.live_plot_activation = QCheckBox(self.centralwidget)
        self.live_plot_activation.setObjectName(u"live_plot_activation")
        self.live_plot_activation.setGeometry(QRect(10, 150, 151, 20))
        self.pause_measure = QPushButton(self.centralwidget)
        self.pause_measure.setObjectName(u"pause_measure")
        self.pause_measure.setGeometry(QRect(10, 230, 151, 24))
        self.continue_measure = QPushButton(self.centralwidget)
        self.continue_measure.setObjectName(u"continue_measure")
        self.continue_measure.setGeometry(QRect(10, 260, 151, 24))
        self.date_time = QLabel(self.centralwidget)
        self.date_time.setObjectName(u"date_time")
        self.date_time.setGeometry(QRect(640, 0, 161, 20))
        self.end_measure = QPushButton(self.centralwidget)
        self.end_measure.setObjectName(u"end_measure")
        self.end_measure.setGeometry(QRect(10, 350, 151, 24))
        self.save_values_xlsx = QPushButton(self.centralwidget)
        self.save_values_xlsx.setObjectName(u"save_values_xlsx")
        self.save_values_xlsx.setGeometry(QRect(10, 440, 151, 24))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(10, 470, 151, 24))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 20, 151, 24))
        self.voltage_plot = VoltagePlot(self.centralwidget)
        self.voltage_plot.setObjectName(u"voltage_plot")
        self.voltage_plot.setGeometry(QRect(170, 30, 621, 481))
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
        self.live_plot_activation.setText(QCoreApplication.translate("MainWindow", u"Plot aktivieren", None))
        self.pause_measure.setText(QCoreApplication.translate("MainWindow", u"Messung anhalten", None))
        self.continue_measure.setText(QCoreApplication.translate("MainWindow", u"Messung fortsetzen", None))
        self.date_time.setText(QCoreApplication.translate("MainWindow", u"Hier Datum, Zeit", None))
        self.end_measure.setText(QCoreApplication.translate("MainWindow", u"Messung abgeschlossen", None))
        self.save_values_xlsx.setText(QCoreApplication.translate("MainWindow", u"Werte speichern (.xlsx)", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Werte speichern (.csv)", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Eichung durchf\u00fchren", None))
    # retranslateUi

