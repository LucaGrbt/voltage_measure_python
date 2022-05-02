# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 11:54:45 2022

@author: LucaGraebenteich
"""

### popup window for saving data with identification of students group

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Save_Error_Window(object):
    
    def setupUi(self, Save_Error_Window):
        Save_Error_Window.setObjectName(u"Save_Warning_Window")
        Save_Error_Window.resize(550, 50)
        self.warn_text = QLabel(Save_Error_Window)
        self.warn_text.setObjectName(u"warn_text")
        self.warn_text.setGeometry(QRect(5, 5, 500, 40))
        
        self.retranslateUi(Save_Error_Window)

        QMetaObject.connectSlotsByName(Save_Error_Window)
        
    def retranslateUi(self, Save_Error_Window):
        Save_Error_Window.setWindowTitle(QCoreApplication.translate("Save_Warning_Window", u"WARNUNG!", None))
        self.warn_text.setText(QCoreApplication.translate("Save_Warning_Window", u"Gruppenname oder andere Identifikation eingeben\nKeine Slashes ( / ) oder ( : ) verwenden", None))
