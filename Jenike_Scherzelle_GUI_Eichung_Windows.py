# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Jenike_Scherzelle_GUI_v01_Eichung.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Calibration_Window(object):
    
    calibration_data = []
    
    def setupUi(self, Calibration_Window):
        Calibration_Window.setObjectName(u"Calibration_Window")
        Calibration_Window.resize(221, 491)
        # show current voltage 
        self.current_voltage = QLabel(Calibration_Window)
        self.current_voltage.setObjectName(u"current_voltage")
        self.current_voltage.setGeometry(QRect(40, 105, 141, 31))
        font = QFont()
        font.setPointSize(10)
        self.current_voltage.setFont(font)
        self.current_voltage.setAlignment(Qt.AlignCenter)
        self.current_voltage.setWordWrap(False)
        # display current voltage from real_time_plot
        self.current_measure_display = QLabel(Calibration_Window)
        self.current_measure_display.setObjectName(u"current_measure_display")
        self.current_measure_display.setGeometry(QRect(40, 140, 141, 31))
        self.current_measure_display.setFont(font)
        self.current_measure_display.setAlignment(Qt.AlignCenter)
        # indicate to put in weight in kilograms and use a dot for decimals instead of a comma
        self.weight_instruction = QLabel(Calibration_Window)
        self.weight_instruction.setObjectName(u"weight_instruction")
        self.weight_instruction.setGeometry(QRect(30, 209, 161, 51))
        self.weight_instruction.setFont(font)
        self.weight_instruction.setAlignment(Qt.AlignCenter)
        ### weight input
        self.current_weight_input = QLineEdit(Calibration_Window)
        self.current_weight_input.setObjectName(u"current_weight_input")
        self.current_weight_input.setGeometry(QRect(40, 269, 141, 31))
        self.current_weight_input.setAlignment(Qt.AlignCenter)
        font1 = QFont()
        font1.setPointSize(12)
        self.current_weight_input.setFont(font1)
        # append weight(x)/voltage(y) pair
        self.append_weight_voltage_pair = QPushButton(Calibration_Window)
        self.append_weight_voltage_pair.setObjectName(u"append_weight_voltage_pair")
        self.append_weight_voltage_pair.setGeometry(QRect(40, 320, 141, 23))
        # indicate to have taken all necessary data before saving the plot/data
        self.gauge_finished = QLabel(Calibration_Window)
        self.gauge_finished.setObjectName(u"gauge_finished")
        self.gauge_finished.setGeometry(QRect(10, 360, 201, 31))
        self.gauge_finished.setAlignment(Qt.AlignCenter)
        # show and save a plot of the calibration curve and calibration data
        self.plot_calibration_curve = QPushButton(Calibration_Window)
        self.plot_calibration_curve.setObjectName(u"plot_calibration_curve")
        self.plot_calibration_curve.setGeometry(QRect(50, 400, 121, 41))
        # delete past calibration data
        self.delete_last_calibration_data = QPushButton(Calibration_Window)
        self.delete_last_calibration_data.setObjectName(u"delete_last_calibration_data")
        self.delete_last_calibration_data.setGeometry(QRect(10, 20, 201, 21))
        # warning calibration start deletes past data
        self.delete_warning = QLabel(Calibration_Window)
        self.delete_warning.setObjectName(u"delete_warning")
        self.delete_warning.setGeometry(QRect(10, 50, 201, 31))
        self.delete_warning.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Calibration_Window)

        QMetaObject.connectSlotsByName(Calibration_Window)
    # setupUi

    def retranslateUi(self, Calibration_Window):
        Calibration_Window.setWindowTitle(QCoreApplication.translate("Calibration_Window", u"Eichkurve", None))
        self.current_voltage.setText(QCoreApplication.translate("Calibration_Window", u"Aktuelle Spannung", None))
        self.current_measure_display.setText(QCoreApplication.translate("Calibration_Window", u"Spannungswert anzeigen", None))
        self.weight_instruction.setText(QCoreApplication.translate("Calibration_Window", u"Gewicht eingeben\n"
"[kg]\n(Nutze Punkt, nicht Komma!)", None))
        self.append_weight_voltage_pair.setText(QCoreApplication.translate("Calibration_Window", u"Messwert aufnehmen", None))
        self.gauge_finished.setText(QCoreApplication.translate("Calibration_Window", u"Alle Messwerte aufgenommen", None))
        self.plot_calibration_curve.setText(QCoreApplication.translate("Calibration_Window", u"Eichkurve anzeigen\n"
"und speichern (.xlsx)", None))
        self.delete_last_calibration_data.setText(QCoreApplication.translate("Calibration_Window", u"Letzte Eichung l\u00f6schen", None))
        self.delete_warning.setText(QCoreApplication.translate("Calibration_Window", u"(Daten der vorangegangenen\n"
"Eichung werden hiermit gel\u00f6scht!)", None))
    # retranslateUi

