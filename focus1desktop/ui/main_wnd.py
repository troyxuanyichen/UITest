from __future__ import division
from __future__ import absolute_import
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QColor, QStyleOptionButton, QLabel, QPixmap

from .round_indicator import RoundIndicator
from .graphs import GraphFlow, GraphAttention, GraphFrequency, GraphHistogram
from focus1desktop.DataProcessor import DataProcessor
from focus1desktop.PackageReceiver import PackageReceiver
from .center_widget import CenterWidget
from . import aux
from .close_button import CloseButton
import thread

# fix length of the windows
_WIDTH = 1425
_HEIGHT = 675
_TITLE_BAR_H = 43


class MainWindow(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.pressed_pt = None
        self.resize(_WIDTH, _HEIGHT)
        aux.set_window_background(self, (0, 0, 0))
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint);

        _CLOSE_BORDER = 4
        self.close_btn = CloseButton(self)
        close_w = _TITLE_BAR_H - _CLOSE_BORDER
        self.close_btn.setFixedSize(close_w, close_w)

        brain_lbl = QLabel(self)
        pic = QPixmap(u"focus1desktop/ui/brain.png")
        brain_lbl.setPixmap(pic)
        brain_lbl.setScaledContents(True)
        brain_lbl.setFixedSize(close_w, close_w)

        focus_lbl = QLabel(u"FOCUS", self)
        fnt = aux.app_font()
        fnt.setPointSize(8)
        focus_lbl.setStyleSheet(u"QLabel { color: white; }")
        focus_lbl.setFont(fnt)

        h_layout = QHBoxLayout()
        h_layout.setMargin(_CLOSE_BORDER)
        h_layout.setSpacing(0)
        h_layout.addWidget(brain_lbl)
        h_layout.addSpacing(10)
        h_layout.addWidget(focus_lbl)
        h_layout.addStretch(1)
        h_layout.addWidget(self.close_btn)

        self.client = ClientArea(parent=self)
        v_layout = QVBoxLayout(self)
        v_layout.setMargin(0)
        v_layout.setSpacing(0)
        v_layout.addItem(h_layout)
        v_layout.addWidget(self.client, 1)
        self.setLayout(v_layout)

    def mousePressEvent(self, event):
        if (event.buttons() == QtCore.Qt.LeftButton):
            self.pressed_pt = event.pos()

    def mouseMoveEvent(self, event):
        if self.pressed_pt:
            new_x = event.globalX()
            new_y = event.globalY()
            self.move(new_x - self.pressed_pt.x(), new_y - self.pressed_pt.y())

    def mouseReleaseEvent(self, event):
        if (event.buttons() == QtCore.Qt.LeftButton):
            self.pressed_pt = None


class ClientArea(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(ClientArea, self).__init__(*args, **kwargs)
        # self.pr = PackageReceiver('192.168.1.101', 8899)  #use this if in STA
        # self.pr = PackageReceiver('10.10.100.254', 8899) #use this if headband is in AP mode
        # self.pr = PackageReceiver('10.1.10.126', 8899) #
        # self.pr = PackageReceiver('10.1.10.74', 8899)  # use this if headband is in STA mode and modify the IP to the correct one, right leg drive
        # self.pr = PackageReceiver('10.1.10.242', 8899) #use this if headband is in STA mode and modify the IP to the two points PCB, 3AF1
        # self.pr = PackageReceiver('10.1.10.127', 8899) #use this if headband is in STA mode for heanband device with pre-filter, sta
        self.pr = PackageReceiver('10.1.10.126',
                                  8899)  # use this if headband is in STA mode for heanband device with pre-filter, sta, real
        self.pr.sendDataToWifi()
        self.dataProcessor = self.pr.dataProcessor
        thread.start_new_thread(self.pr.startConnecting, ())

    def resizeEvent(self, event):
        _CENTERW_W = 270
        height = self.rect().height()
        _BORDER = 15
        # graphs overlap to center widget
        _CENTER_OVER = 20

        aux.set_window_background(self, (255, 255, 255))
        self.setAutoFillBackground(True)

        self.centerw = CenterWidget(parent=self, round_ind_size=150, outer_color=QtGui.QColor(245, 245, 245))
        self.centerw.move((_WIDTH - _CENTERW_W) / 2, (height - _CENTERW_W) / 2)
        self.centerw.resize(_CENTERW_W, _CENTERW_W)
        self.centerw.value = 92

        # self.dproc = dataProcessor()

        self.graphAttention = GraphAttention(self)
        self.graphAttention.move(_BORDER, _BORDER)
        graph_w = (_WIDTH - _CENTERW_W) / 2 - _BORDER + _CENTER_OVER
        graph_h = (height - _CENTERW_W) / 2 - _BORDER + _CENTER_OVER
        self.graphAttention.resize(graph_w, graph_h)

        self.graphFlow = GraphFlow(self)
        flow_x = _WIDTH / 2 + _CENTERW_W / 2 - _CENTER_OVER
        self.graphFlow.move(flow_x, _BORDER)
        self.graphFlow.resize(graph_w, graph_h)

        self.graphFrequency = GraphFrequency(self)
        freq_y = height / 2 + _CENTERW_W / 2 - _CENTER_OVER
        self.graphFrequency.move(_BORDER, freq_y)
        self.graphFrequency.resize(graph_w, graph_h)

        self.graphHistogram = GraphHistogram(self)
        self.graphHistogram.move(flow_x, freq_y)
        self.graphHistogram.resize(graph_w, graph_h)

        self.setWindowTitle(u"Focus 1")

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update)
        self._timer.start(100)

        u""" Background image
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QPixmap("focus1desktop/ui/lightpaperfibers.png"))
        palette.setBrush(QtGui.QPalette.Background, brush)
        self.setPalette(palette)
        """

        self.a = []

    def update(self):
        self.centerw.text = self.dataProcessor.message

        self.graphFlow.setData(self.dataProcessor.rawdata_array_whole)
        self.graphAttention.setData(self.dataProcessor.scalEngIndBuff)
        self.graphFrequency.setData(self.dataProcessor.rawfft_x[:100], self.dataProcessor.rawfft_y[:100])
        self.graphHistogram.setData(self.dataProcessor.histox, self.dataProcessor.histoy)
        if len(self.dataProcessor.scalEngIndBuff) != 0:
            self.centerw.value = int(self.dataProcessor.scalEngIndBuff[-1])
