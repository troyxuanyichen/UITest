
from __future__ import absolute_import
import sys

from PyQt4 import QtGui, QtCore 

from .ui.main_wnd import MainWindow
from .ui.aux import logo_file

def run():  
   app = QtGui.QApplication(sys.argv)
   icon = QtGui.QIcon()
   icon.addFile(logo_file(), QtCore.QSize(32, 32))
   app.setWindowIcon(icon)
   window = MainWindow()
   window.show()
   return app.exec_()

