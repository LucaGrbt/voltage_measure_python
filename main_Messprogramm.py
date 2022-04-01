# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 22:27:19 2022

@author: LucaGraebenteich
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from Jenike_Scherzelle_GUI import Ui_MainWindow

class Messprogramm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Messprogramm, self).__init__(parent)
        self.setupUi(self)
        
    
if __name__ == '__main__':        
    app = QApplication([])
    messprogramm = Messprogramm()
    messprogramm.show()
    app.exec()



