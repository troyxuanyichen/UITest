
from __future__ import absolute_import
from PyQt4.QtGui import QFont, QColor, QLabel
from PyQt4 import QtGui

def label(text, px_size):
   lbl = QLabel(text)
   font = app_font()
   font.setPixelSize(px_size)
   lbl.setFont(font)
   palette = QtGui.QPalette()
   palette.setColor(QtGui.QPalette.Foreground, fore_color())
   lbl.setPalette(palette)
   return lbl

def logo_file():
    return u"focus1desktop/ui/brain.png"

def video_file():
    return u"focus1desktop/ui/ces_demo_video.mp4"

def app_font():        
    #font = QFont("Mukti Narrow", 22)
    #font.setStyleHint(QFont.Monospace)
    fontFile = u"focus1desktop/ui/submarine.ttf" 
    fontdb = QtGui.QFontDatabase() 
    id = fontdb.addApplicationFont(fontFile) 
    family = fontdb.applicationFontFamilies(id) 
    font = QtGui.QFont(family[0]) 
    font.setPixelSize(40)
    return font

def fore_color():
    return QColor(66, 127, 120)

def back_light_color():
    return QColor(22, 38, 46) 

def back_color():
    return QColor(16, 22, 29)   

def fore_bright_color():
    return QColor(4, 251, 236)

def set_window_background(window, color):
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Background, color)
    window.setPalette(palette)


