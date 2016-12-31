
from __future__ import division
from __future__ import absolute_import
import math

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPen, QBrush, QConicalGradient, QColor, QFont
from PyQt4.QtCore import QPropertyAnimation, QEasingCurve
from .aux import app_font, back_light_color, fore_color, fore_bright_color

class RoundIndicator(QtGui.QWidget):
    _line_width = 15 

    def __init__(self, *args, **kwargs):
        super(RoundIndicator, self).__init__(*args, **kwargs)
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        if new_val > 100:
            new_val = 100
        if new_val < 0:
            new_val = 0
        self._value = new_val
        self.update()

    def paintEvent(self, event):
        #pt = QtGui.QPainter(self.viewport())
        pt = QtGui.QPainter(self)
        #pt.begin(self)
        pt.setRenderHint(QtGui.QPainter.Antialiasing, True)

        drawRect = self.rect()
        u"""Otherwise the line will be cut by rect borders"""
        drawRect.adjust(self._line_width / 2, self._line_width / 2, -self._line_width / 2, -self._line_width / 2)

        u"""INNER CIRCLE"""

        pt.setPen(QPen(back_light_color()))
        pt.setBrush(QBrush(back_light_color()))
        pt.drawEllipse(drawRect)

        u"""LINE"""

        main_color = fore_color()
        conical = QConicalGradient(self.rect().center().x(), self.rect().center().y(), 90) 
        conical.setColorAt(0.999, main_color)
        #main_color = QColor(*fore_bright_color())
        conical.setColorAt((100 - self._value) / 100, main_color)

        pen = QPen(QBrush(conical), self._line_width)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pt.setPen(pen)

        u"""Calculating the angle to offset line start/end. otherwise gradient start falls inside line's beginning cap"""
        radius = drawRect.width() / 2
        capAngle = math.degrees(math.acos(1 - self._line_width ** 2 / (2 * radius ** 2)))

        start = (90 - capAngle / 2) * 16
        u"""offsetted backwards"""
        end = - (360 - capAngle * 1.1) / 100 * self._value * 16
        pt.drawArc(drawRect, start, end if end else 1)

        u"""NUMBER"""

        pt.setPen(QPen(main_color))
        pt.setFont(app_font())
        pt.drawText(self.rect(), QtCore.Qt.AlignCenter, unicode(self._value))

        super(RoundIndicator, self).paintEvent(event)


