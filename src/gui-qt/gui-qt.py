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
                         
import system
import flow

__version__ = '0.0.1'
 
from mpl import Ui_MainWindow
 
class MainWindow(QMainWindow, Ui_MainWindow):
    
    
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)

        self.main_frame = Ui_MainWindow()
        self.main_frame.setupUi(self)
        
        
        ## TODO: check the input strings for whitespaces or put default values
        
        #self.workhorse = system.system_def(float(self.main_frame.dim_x.text()), 
        #                                   float(self.main_frame.dim_y.text()), float(self.main_frame.spacing.text()), 
        #                                   0.0, float(self.main_frame.k.text()), float(self.main_frame.n.text()))
        
        #self.workhorse.fixed_boundary_conditions(float(self.main_frame.head_up.text()), float(self.main_frame.head_down.text())) 
        
        #self.flow = flow.flow_calc(self.main_frame.max_iter, self.main_frame.limit_convergence, flow_system) 
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
            
    
    frame.show()
    app.exec_()
    
    
    
    
    
    
