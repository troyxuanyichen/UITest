
from PyQt4 import QtGui
from PyQt4.QtGui import QPushButton, QIcon 

class CloseButton(QPushButton):
    def __init__(self, window):
        super().__init__(parent=window)
        self.icon = QIcon("focus1desktop/ui/fi-power.png")
        self.icon_pressed = QIcon("focus1desktop/ui/fi-pressed.png")
        self.setIcon(self.icon)
        self.setFlat(True)
        self.window = window
        #self.setAutoFillBackground(True)

    def mousePressEvent(self, event):
        #super().mousePressEvent(event)
        self.setIcon(self.icon_pressed)
        event.accept()

    def mouseReleaseEvent(self, event):
        #super().mouseReleaseEvent(event)
        if (self.rect().contains(event.pos())):
            self.window.close()
        self.setIcon(self.icon)
        event.accept()

    def mouseMoveEvent(self, event):
        event.accept()
    

