from __future__ import absolute_import
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QColor, QStyleOptionButton, QLabel, QPixmap, QGridLayout, QSizePolicy

from .round_indicator import RoundIndicator
from .graphs import GraphFlow, GraphAttention, GraphFrequency, GraphHistogram
from focus1desktop.DataProcessor import DataProcessor
from focus1desktop.PackageReceiver import PackageReceiver
from .center_widget import CenterWidget
from . import aux
from .close_button import CloseButton
import thread

_WIDTH = 1350
_HEIGHT = 675
_TITLE_BAR_H = 43
_LEFT_MARGIN = 120


class MainWindow(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.pressed_pt = None

        self.resize(_WIDTH, _HEIGHT)
        aux.set_window_background(self, aux.back_light_color())  # QColor(0, 0, 0))
        # self.setStyleSheet("MainWindow { background: #000000 }")

        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint);

        _CLOSE_BORDER = 4
        self.close_btn = CloseButton(self)
        close_w = _TITLE_BAR_H - _CLOSE_BORDER
        self.close_btn.setFixedSize(close_w, close_w)

        brain_lbl = QLabel(self)
        pic = QPixmap(aux.logo_file())
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
        # self.pr = PackageReceiver('10.1.10.126',
        #                           8899)  # use this if headband is in STA mode for heanband device with pre-filter, sta, real
        self.pr = PackageReceiver('10.10.100.254',
                                  8899)  # use this if headband is in STA mode for heanband device with pre-filter, sta, real
        self.pr.sendDataToWifi()
        self.dataProcessor = self.pr.dataProcessor
        thread.start_new_thread(self.pr.startConnecting, ())

    def resizeEvent(self, event):
        _ROUND_IND = 150
        _BORDER = 15

        aux.set_window_background(self, aux.back_color())
        self.setAutoFillBackground(True)

        self.centerw = CenterWidget(parent=self, left_margin=_LEFT_MARGIN)

        # self.dproc = DataProcessor()

        self.graphAttention = GraphAttention(self)
        self.graphFlow = GraphFlow(self)
        self.graphFrequency = GraphFrequency(self)
        self.graphHistogram = GraphHistogram(self)

        self.round_ind = RoundIndicator(self)
        self.round_ind.setFixedSize(_ROUND_IND, _ROUND_IND)

        round_tag = aux.label(u"Attention", 14)
        round_tag.setParent(self)
        v_round = QVBoxLayout()
        v_round.addStretch(1)
        v_round.addWidget(round_tag, 0, QtCore.Qt.AlignCenter)
        v_round.addSpacing(10)
        v_round.addWidget(self.round_ind, 0, QtCore.Qt.AlignCenter)
        v_round.addStretch(1)

        g_layout = QGridLayout()
        self.setLayout(g_layout)
        g_layout.setContentsMargins(_BORDER, _BORDER, _BORDER, _BORDER)
        g_layout.addWidget(self.centerw, 0, 0)
        g_layout.addWidget(self.graphAttention, 0, 1)
        g_layout.addWidget(self.graphFlow, 0, 2)
        g_layout.addLayout(v_round, 1, 0)
        g_layout.addWidget(self.graphFrequency, 1, 1)
        g_layout.addWidget(self.graphHistogram, 1, 2)
        g_layout.setColumnStretch(0, 25)
        g_layout.setColumnStretch(1, 37)
        g_layout.setColumnStretch(2, 37)
        g_layout.setRowStretch(0, 0.5)
        self.updateGeometry()

        self.setWindowTitle(u"Focus 1")

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update)
        self._timer.start(200)

        u""" Background image
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QPixmap("focus1desktop/ui/back.png"))
        palette.setBrush(QtGui.QPalette.Background, brush)
        self.setPalette(palette)
        """
        # self.setStyleSheet("QWidget { background: url(focus1desktop/ui/back.png); }")

        self.a = []

    def update(self):
        self.round_ind.text = self.dataProcessor.message

        self.graphFlow.setData(self.dataProcessor.rawdata_array_whole)
        self.graphAttention.setData(self.dataProcessor.scalEngIndBuff)
        self.graphFrequency.setData(self.dataProcessor.rawfft_x[:100], self.dataProcessor.rawfft_y[:100])
        self.graphHistogram.setData(self.dataProcessor.histox, self.dataProcessor.histoy)
        if len(self.dataProcessor.scalEngIndBuff) != 0:
            self.round_ind.value = int(self.dataProcessor.scalEngIndBuff[-1])
