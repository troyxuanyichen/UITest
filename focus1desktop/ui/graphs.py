from __future__ import division
from __future__ import absolute_import
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFont, QLabel, QPen, QColor, QBrush, QConicalGradient, QLinearGradient
from PyQt4.QtCore import QPointF
import pyqtgraph
from pyqtgraph import mkPen

from .aux import app_font, fore_color, fore_bright_color, back_light_color, back_color

CURVE_WIDTH = 2  # This is in pixels for all graphs not including Attention
ATTENTION_CURVE_WIDTH = 0.8  # This is in graph coordinates!
GRAPH_FLOW_MAX_Y_MODULE = 100
GRAPH_FREQUENCY_MAX_Y = 5000
GRAPH_HISTOGRAM_MAX_Y = 10000
GRAPH_ATTENTION_MAX_Y = 200
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
        axis_top = pyqtgraph.AxisItem(orientation=u'top', pen=fore_color())
        axis_y = pyqtgraph.AxisItem(orientation=u'left', pen=fore_color())
        axis_right = pyqtgraph.AxisItem(orientation=u'right', pen=fore_color())
        tfont = app_font()
        tfont.setPixelSize(12)

        axis_top.setStyle(tickLength=0, showValues=False)
        axis_right.setStyle(tickLength=0, showValues=False)

        axis_x.tickFont = tfont
        axis_x.setStyle(tickLength=0)
        self.modify_axis_x(axis_x)

        axis_y.tickFont = tfont
        axis_y.setStyle(tickLength=0)
        self.modify_axis_y(axis_y)

        super(GraphBase, self).__init__(parent=parent, background=None,
                                        axisItems={u'top': axis_top, u'bottom': axis_x, u'left': axis_y,
                                                   u'right': axis_right}, title=u" ")
        self.showAxis(u'top')
        self.showAxis(u'right')

        self.title_lbl = QLabel(title, self)
        font = app_font()
        font.setPixelSize(20)
        self.title_lbl.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, fore_color())
        self.title_lbl.setPalette(palette)

        pyqtgraph.setConfigOptions(antialias=True)
        self.curve = self.plot(pen=self.pen(), **self.plot_args())

    def resizeEvent(self, event):
        if event:
            super(GraphBase, self).resizeEvent(event)
            self.title_lbl.move((self.rect().width() - self.title_lbl.rect().width()) / 2, 0)
            # print(self.title_lbl)
            event.accept()

    def setData(self, *args):
        if u'curve' in self.__dict__:
            self.curve.setData(*args)

    def pen(self):
        return mkPen(fore_bright_color(), width=CURVE_WIDTH)

    def plot_args(self):
        return {}


class GraphFlow(GraphBase): # second
    def __init__(self, parent):
        super(GraphFlow, self).__init__(parent, title=u"Flow Data")
        # self.plotItem.getViewBox().setYRange(-GRAPH_FLOW_MAX_Y_MODULE, GRAPH_FLOW_MAX_Y_MODULE)
        # self.plotItem.getViewBox().setXRange(0, GRAPH_FLOW_MAX_X)

    def modify_axis_x(self, axis):
        axis.setTickSpacing(GRAPH_FLOW_MAX_X, GRAPH_FLOW_MAX_X)

    def modify_axis_y(self, axis):
        axis.setTickSpacing(GRAPH_FLOW_MAX_Y_MODULE, GRAPH_FLOW_MAX_Y_MODULE)


class GraphAttention(GraphBase): # first
    def __init__(self, parent):
        super(GraphAttention, self).__init__(parent, title=u"Attention")
        view_box = self.plotItem.getViewBox()
        #view_box.setYRange(0, GRAPH_ATTENTION_MAX_Y)
        view_box.setXRange(0, GRAPH_ATTENTION_MAX_X)

        self.curve_logic_width = ATTENTION_CURVE_WIDTH

    def modify_axis_x(self, axis):
        axis.setTickSpacing(GRAPH_ATTENTION_MAX_X, GRAPH_ATTENTION_MAX_X)

    def modify_axis_y(self, axis):
        axis.setTickSpacing(GRAPH_ATTENTION_MAX_Y, GRAPH_ATTENTION_MAX_Y)


class GraphFrequency(GraphBase): # third
    def __init__(self, parent):
        super(GraphFrequency, self).__init__(parent, title=u"Frequency Spectrum")
        # self.plotItem.getViewBox().setYRange(0, GRAPH_FREQUENCY_MAX_Y)
        # self.plotItem.getViewBox().setXRange(0, GRAPH_FREQUENCY_MAX_X)

    def modify_axis_x(self, axis):
        axis.setTickSpacing(GRAPH_FREQUENCY_MAX_X, GRAPH_FREQUENCY_MAX_X)
        # axis.setTickSpacing(34, 10)

    def modify_axis_y(self, axis):
        axis.setTickSpacing(GRAPH_FREQUENCY_MAX_Y, GRAPH_FREQUENCY_MAX_Y)
        # axis.setTickSpacing(200, 200)


class GraphHistogram(GraphBase): # forth
    def __init__(self, parent):
        super(GraphHistogram, self).__init__(parent, title=u"Histogram")
        # self.plotItem.getViewBox().setYRange(0, GRAPH_HISTOGRAM_MAX_Y)
        # self.plotItem.getViewBox().setXRange(0, GRAPH_HISTOGRAM_MAX_X)

    def modify_axis_x(self, axis):
        axis.setTickSpacing(GRAPH_HISTOGRAM_MAX_X, GRAPH_HISTOGRAM_MAX_X)
        # axis.setTickSpacing(4, 4)

    def modify_axis_y(self, axis):
        axis.setTickSpacing(GRAPH_HISTOGRAM_MAX_Y, GRAPH_HISTOGRAM_MAX_Y)
        # axis.setTickSpacing(10000, 10000)

    def pen(self):
        return QPen(fore_color())

    def plot_args(self):
        return {u'fillStep': True, u'stepMode': False, u'fillLevel': 0, u'brush': QBrush(back_light_color())}
