
import math

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPen, QBrush, QConicalGradient, QColor, QFont
from PyQt4.QtCore import QPropertyAnimation, QEasingCurve
from .aux import app_font

"""
QColor getColor(qreal key) const
{
        // key must belong to [0,1]
            key = Clip(key, 0.0, 1.0) ;

                // directly get color if known
                    if(controlPoints().contains(key))
                            {
                                        return controlPoints().value(key) ;
                                            }

                                                // else, emulate a linear gradient
                                                    QPropertyAnimation interpolator ;
                                                        const qreal granularite = 100.0 ;
                                                            interpolator.setEasingCurve(QEasingCurve::Linear) ;
                                                                interpolator.setDuration(granularite) ;
                                                                    foreach( qreal key, controlPoints().keys() )
                                                                        {
                                                                                    interpolator.setKeyValueAt(key, controlPoints().value(key)) ;
                                                                                        }
                                                                                            interpolator.setCurrentTime(key*granularite) ;
                                                                                                return interpolator.currentValue().value<QColor>() ;
}
"""

class GradientEmulator(object):
    def __init__(self):
        self.anim = QPropertyAnimation()
        self.anim.setEasingCurve(QEasingCurve.Linear)
        self.anim.setDuration(100)

    def setColorAt(self, x, color):
        self.anim.setKeyValueAt(x, color)

    def getAt(self, x):
        self.anim.setCurrentTime(x * 100)
        return self.anim.currentValue()

class RoundIndicator(QtGui.QWidget):
    _line_width = 15 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gradient = GradientEmulator()
        self.gradient.setColorAt(0, QColor(255, 0, 0)) 
        self.gradient.setColorAt(0.3, QColor(255, 0, 0)) 
        self.gradient.setColorAt(0.5, QColor(255, 255, 0))
        self.gradient.setColorAt(0.65, QColor(255, 255, 0))
        self.gradient.setColorAt(0.75, QColor(98, 178, 213))
        self.gradient.setColorAt(1, QColor(98, 178, 213))

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
        """Otherwise the line will be cut by rect borders"""
        drawRect.adjust(self._line_width / 2, self._line_width / 2, -self._line_width / 2, -self._line_width / 2)

        """INNER CIRCLE"""

        pt.setPen(QPen(QtCore.Qt.white))
        pt.setBrush(QBrush(QtCore.Qt.white))
        pt.drawEllipse(drawRect)

        """LINE"""

        main_color = self.gradient.getAt((100 - self._value) / 100)
        conical = QConicalGradient(self.rect().center().x(), self.rect().center().y(), 90) 
        conical.setColorAt(0.999, main_color)
        main_color = main_color.darker(120)
        print(self._value / 100)
        conical.setColorAt((100 - self._value) / 100, main_color)
        #conical.setColorAt(1, QtCore.Qt.green)

        pen = QPen(QBrush(conical), self._line_width)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pt.setPen(pen)

        """Calculating the angle to offset line start/end. otherwise gradient start falls inside line's beginning cap"""
        radius = drawRect.width() / 2
        capAngle = math.degrees(math.acos(1 - self._line_width ** 2 / (2 * radius ** 2)))

        start = (90 - capAngle / 2) * 16
        """offsetted backwards"""
        end = - (360 - capAngle * 1.1) / 100 * self._value * 16
        pt.drawArc(drawRect, start, end if end else 1)

        """NUMBER"""

        pt.setPen(QPen(main_color))
        pt.setFont(app_font())
        pt.drawText(self.rect(), QtCore.Qt.AlignCenter, str(self._value))

        super().paintEvent(event)


