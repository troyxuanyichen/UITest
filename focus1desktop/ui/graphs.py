from __future__ import division
from __future__ import absolute_import
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFont, QLabel, QPen, QColor, QBrush, QConicalGradient, QLinearGradient
from PyQt4.QtCore import QPointF
import pyqtgraph
from pyqtgraph import mkPen

from .aux import app_font, fore_color

CURVE_WIDTH = 3  # This is in pixels for all graphs not including Attention
ATTENTION_CURVE_WIDTH = 0.8  # This is in graph coordinates!
GRAPH_FLOW_MAX_Y_MODULE = 2
GRAPH_FREQUENCY_MAX_Y = 800
GRAPH_HISTOGRAM_MAX_Y = 40000
GRAPH_ATTENTION_MAX_Y = 100
GRAPH_FLOW_MAX_X = 500
GRAPH_FREQUENCY_MAX_X = 34
GRAPH_HISTOGRAM_MAX_X = 20
GRAPH_ATTENTION_MAX_X = 200


# If you want a graph to automatically fit the range by data, remove the corresponding setXRange() call

class GraphBase(pyqtgraph.PlotWidget):
    def __init__(self, parent, **_3to2kwargs):
        if 'title' in _3to2kwargs:
            title = _3to2kwargs['title']; del _3to2kwargs['title']
        else:
            title = u""
        axis_x = pyqtgraph.AxisItem(orientation=u'bottom', pen=fore_color())
        axis_y = pyqtgraph.AxisItem(orientation=u'left', pen=fore_color())
        tfont = app_font()
        tfont.setPointSize(8)

        axis_x.tickFont = tfont
        axis_x.setStyle(tickLength=0)
        self.modify_axis_x(axis_x)

        axis_y.tickFont = tfont
        axis_y.setStyle(tickLength=0)
        self.modify_axis_y(axis_y)

        super(GraphBase, self).__init__(parent=parent, background=(255, 255, 255),
                                        axisItems={u'bottom': axis_x, u'left': axis_y}, title=u" ")

        self.title_lbl = QLabel(title, self)
        font = app_font()
        font.setPointSize(10)
        self.title_lbl.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, QtGui.QColor(*fore_color()))
        self.title_lbl.setPalette(palette)

        pyqtgraph.setConfigOptions(antialias=True)

    def showEvent(self, event):
        self.title_lbl.move((self.rect().width() - self.title_lbl.rect().width()) / 2, 0)
        self.curve = self.plot(pen=self.pen(), **self.plot_args())

    def setData(self, *args):
        if u'curve' in self.__dict__:
            # #########
            # print '*args'
            # print len(*args)  # two arguments
            # #########
            self.curve.setData(*args)

    def pen(self):
        return mkPen(u'b', width=CURVE_WIDTH)

    def plot_args(self):
        return {}


class GraphFlow(GraphBase):
    def __init__(self, parent):
        super(GraphFlow, self).__init__(parent, title=u"Flow Data")
        self.plotItem.getViewBox().setYRange(-GRAPH_FLOW_MAX_Y_MODULE, GRAPH_FLOW_MAX_Y_MODULE)
        self.plotItem.getViewBox().setXRange(0, GRAPH_FLOW_MAX_X)

    def modify_axis_x(self, axis):
        axis.setTickSpacing(100, 100)

    def modify_axis_y(self, axis):
        axis.setTickSpacing(1, 1)


# class GraphAttention(GraphBase):
#     def __init__(self, parent):
#         super(GraphAttention, self).__init__(parent, title=u"Attention")
#
#     def showEvent(self, event):
#         view_box = self.plotItem.getViewBox()
#         # view_box.setYRange(0, GRAPH_ATTENTION_MAX_Y)
#         # view_box.setXRange(0, GRAPH_ATTENTION_MAX_X)
#         pt_from = QPointF(0, GRAPH_ATTENTION_MAX_Y)
#         pt_to = QPointF(0, 0)
#         self.gradient = QLinearGradient(pt_from, pt_to)
#         self.gradient.setColorAt(0.3, QtCore.Qt.red)
#         self.gradient.setColorAt(0.5, QtCore.Qt.yellow)
#         self.gradient.setColorAt(0.65, QtCore.Qt.yellow)
#         self.gradient.setColorAt(0.75, QColor(98, 178, 213))
#         self.brush = QBrush(self.gradient)
#
#         self.curve_logic_width = ATTENTION_CURVE_WIDTH
#
#         super(GraphAttention, self).showEvent(event)
#
#     def modify_axis_x(self, axis):
#         axis.setTickSpacing(40, 40)
#
#     def modify_axis_y(self, axis):
#         axis.setTickSpacing(20, 20)
#
#     def pen(self):
#         return QPen(self.brush, self.curve_logic_width)

class GraphAttention(GraphBase):

    def __init__(self, parent):
        super(GraphAttention, self).__init__(parent, title=u"Attention")

    def showEvent(self, event):
        view_box = self.plotItem.getViewBox()
        view_box.setYRange(0, GRAPH_ATTENTION_MAX_Y)
        view_box.setXRange(0, GRAPH_ATTENTION_MAX_X)
        pt_from = QPointF(0, GRAPH_ATTENTION_MAX_Y)
        pt_to = QPointF(0, 0)

        self.curve_logic_width = ATTENTION_CURVE_WIDTH

        super(GraphAttention, self).showEvent(event)

    def modify_axis_x(self, axis):
        axis.setTickSpacing(40, 40)

    def modify_axis_y(self, axis):
        axis.setTickSpacing(20, 20)

    def setData(self, *args):
        super(GraphAttention, self).setData([10, 40, 90])

class GraphFrequency(GraphBase):
    def __init__(self, parent):
        super(GraphFrequency, self).__init__(parent, title=u"Frequency Spectrum")
        self.plotItem.getViewBox().setYRange(0, GRAPH_FREQUENCY_MAX_Y)
        self.plotItem.getViewBox().setXRange(0, GRAPH_FREQUENCY_MAX_X)

    def modify_axis_x(self, axis):
        axis.setTickSpacing(34, 10)

    def modify_axis_y(self, axis):
        axis.setTickSpacing(200, 200)


class GraphHistogram(GraphBase):
    def __init__(self, parent):
        super(GraphHistogram, self).__init__(parent, title=u"Histogram")
        self.plotItem.getViewBox().setYRange(0, GRAPH_HISTOGRAM_MAX_Y)
        self.plotItem.getViewBox().setXRange(0, GRAPH_HISTOGRAM_MAX_X)

    def modify_axis_x(self, axis):
        axis.setTickSpacing(4, 4)

    def modify_axis_y(self, axis):
        axis.setTickSpacing(10000, 10000)

    def plot_args(self):
        return {u'fillStep': True, u'stepMode': True, u'fillLevel': 0, u'brush': (0, 0, 200)} # step mode
