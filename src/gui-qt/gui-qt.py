'''
Created on 18/10/2012

@author: Ivan Marin
@contact: ispmarin@gmail.com
'''

import sys
import platform

import numpy as np
import PySide
from PySide import QtCore
from PySide.QtGui import QApplication, QMainWindow, QTextEdit,\
                         QPushButton,  QMessageBox, QWidget, QVBoxLayout
                         


__version__ = '0.0.1'
 
from mpl import Ui_MainWindow
 
class MainWindow(QMainWindow, Ui_MainWindow):
    
    
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)

        self.main_frame = Ui_MainWindow()
        self.main_frame.setupUi(self)
        
        
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
            
    
    frame.show()
    app.exec_()
    
    
    
    
    
    
