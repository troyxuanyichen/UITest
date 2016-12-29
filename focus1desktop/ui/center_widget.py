
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPen, QBrush, QColor, QFont, QWidget, QLabel

from .round_indicator import RoundIndicator
from .aux import app_font, fore_color


class CenterWidget(QWidget):
    def __init__(self, parent, *, round_ind_size, outer_color):
       super().__init__(parent)
       self.outer_color = outer_color
       self.round_ind_size = round_ind_size
       self.round_ind = RoundIndicator(self)
       self.round_ind.resize(round_ind_size, round_ind_size)
       self.statusLbl = QLabel("Disconnected",  self)
       font = app_font()
       font.setPointSize(16)
       self.statusLbl.setFont(font)
       palette = QtGui.QPalette()
       palette.setColor(QtGui.QPalette.Foreground, QColor(*fore_color()))
       self.statusLbl.setPalette(palette)

    @property
    def text(self):
        pass
    @text.setter
    def text(self, value):
        self.statusLbl.setText(value)
        self.layout()

    @property
    def value(self):
        pass
    @text.setter
    def value(self, value):
        self.round_ind.value = value

    def showEvent(self, event):
        self.layout()

    def layout(self):
        w_rect = self.rect()
        round_y = w_rect.center().y() - self.round_ind_size / 2
        self.round_ind.move(w_rect.center().x() - self.round_ind_size / 2, round_y)
        self.statusLbl.adjustSize()
        lbl_rect = self.statusLbl.rect()
        self.statusLbl.move(w_rect.center().x() - self.statusLbl.width() / 2, round_y + self.round_ind_size - lbl_rect.height() / 4.5)
        #self.statusLbl.hide()

    def paintEvent(self, event): 
        pt = QtGui.QPainter(self)
        pt.setRenderHint(QtGui.QPainter.Antialiasing, True)

        widget_rect = self.rect()
        pt.setBrush(self.outer_color)
        pt.setPen(self.outer_color)
        pt.drawEllipse(widget_rect)

           
