
import sys

from PyQt4 import QtGui 

from .ui.main_wnd import MainWindow

def run():  
   app = QtGui.QApplication(sys.argv)
   window = MainWindow()
   window.show()
   return app.exec_()

