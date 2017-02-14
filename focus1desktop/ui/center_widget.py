from __future__ import absolute_import
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QColor, QFont, QWidget, QLabel, QVBoxLayout, QPixmap, QSizePolicy, QHBoxLayout
from .round_indicator import RoundIndicator
from .aux import app_font, fore_color, video_file
from . import aux

class PixmapLabel(QLabel):
    def __init__(self, parent, pixmap):
        super(PixmapLabel, self).__init__(parent=parent)
        self.pixmap = pixmap

    def resizeEvent(self, event):
        self.setPixmap(self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


class CenterWidget(QWidget):
    def __init__(self, parent, left_margin):
        super(CenterWidget, self).__init__(parent)

        self.statusLbl = QLabel(u"Disonnected", self)
        self.statusLbl.setWordWrap(True)
        font = app_font()
        font.setPixelSize(24)
        self.statusLbl.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, fore_color())
        self.statusLbl.setPalette(palette)

        self.statusTag = QLabel(u"Status", self)
        font.setPixelSize(14)
        self.statusTag.setFont(font)
        self.statusTag.setPalette(palette)

        # video
        # brain_lbl = QLabel(self)
        # videofrom = QtGui.QWidget()
        # # videofrom.setWindowTitle('Video Player')
        # videofrom.resize(400, 400)
        # player = phonon.VideoPlayer(phonon.VideoCategory, videofrom)
        # player.load(phonon.MediaSource(aux.video_file()))
        # player.play()
        # videofrom.show()
        pic = QPixmap(u"focus1desktop/ui/device.png")
        device_img = PixmapLabel(self, pic)
        # VideoPlayer = phonon.VideoPlayer()
        # media = phonon.Mediasource(aux.video_file())
        # VideoPlayer.load(media)
        # VideoPlayer.play()
        # VideoPlayer.show()

        v_layout = QVBoxLayout()
        v_layout.setSpacing(0)
        self.setLayout(v_layout)

        # v_img = QHBoxLayout()
        # v_img.addWidget(device_img, 1)
        # v_img.setAlignment(QtCore.Qt.AlignCenter)
        # v_layout.addLayout(v_img, 1)
        v_layout.addWidget(device_img, 4)

        # v_layout.addSpacing(20)
        v_text = QVBoxLayout()
        v_text.addWidget(self.statusTag, 0, QtCore.Qt.AlignLeft)
        v_text.addWidget(self.statusLbl, 0, QtCore.Qt.AlignLeft)
        v_text.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addLayout(v_text, 1)
        v_layout.setContentsMargins(left_margin, 40, 40, 40)

    @property
    def text(self):
        pass

    @text.setter
    def text(self, value):
        self.statusLbl.setText(value)
        self.layout()
