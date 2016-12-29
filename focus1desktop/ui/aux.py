
from PyQt4.QtGui import QFont
from PyQt4 import QtGui

def app_font():        
    font = QFont("Mukti Narrow", 22)
    font.setStyleHint(QFont.Monospace)
    return font

def fore_color():
    return (110, 110, 110)

def set_window_background(window, color):
    palette = QtGui.QPalette()
    color = QtGui.QColor(*color)
    palette.setColor(QtGui.QPalette.Background, color)
    window.setPalette(palette)


