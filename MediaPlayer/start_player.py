import os

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QDir, QUrl, QRectF
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtWidgets import QMainWindow, QSplitter, QMenu, QStyle, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from ConfigApplication.ConfigApplication import ConfigApp
from MediaPlayer import Ui_MainWindow


class PlayerScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conf = ConfigApp("media.ini")
        self.setup_gui()

    def resizeEvent(self, event):  # on utilise cette méthode car les flags ne marchent pas avec QMediaPlayer
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        reg = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(reg)

    def setup_gui(self):
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        # videoWidget.resize(500,400)
        # videoWidget.move(100,90)

        self.verticalScreen = QtWidgets.QVBoxLayout(self.ui.screen)

        self.verticalScreen.setContentsMargins(0, 0, 0, 0)
        self.verticalScreen.setSpacing(0)
        self.verticalScreen.setObjectName("verticalScreen")
        self.verticalScreen.addWidget(videoWidget)

        self.ui.slider_position.sliderMoved.connect(self.setPosition)

        self.ui.play.setEnabled(False)
        self.ui.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.play.clicked.connect(self.play)

        self.ui.stop.setEnabled(True)
        self.ui.stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.ui.stop.clicked.connect(self.stop)

        self.ui.next.setEnabled(False)
        self.ui.next.clicked.connect(self.next)

        self.ui.prev.setEnabled(False)
        self.ui.prev.clicked.connect(self.prev)

        self.ui.video.clicked.connect(self.open_video)
        self.ui.audio.clicked.connect(self.open_music)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.mediaPlayer.setVolume(50)
        self.ui.slider_vol.setValue(self.mediaPlayer.volume())

        self.ui.pushButton_close.clicked.connect(self.close_window)
        self.ui.slider_vol.setRange(0, 100)
        self.ui.slider_vol.valueChanged.connect(self.set_volume)
        self.ui.slider_vol.setValue(50)

        self.offset = None

    def eventFilter(self, obj, event):
        if obj == self.ui.centralwidget:

            if event.type() == QtCore.QEvent.KeyRelease:  # jamais sur key down
                if event.key() == QtCore.Qt.Key_Return:
                    print("enter pressed")

                if event.key() == QtCore.Qt.Key_Up:
                    print("enter pressed")

                if event.key() == QtCore.Qt.Key_Down:
                    print("enter pressed")

        return super(QMainWindow, self).eventFilter(obj, event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.offset = None
        super().mouseReleaseEvent(event)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

        self.ui.next.setEnabled(True)
        self.ui.prev.setEnabled(True)
        milliseconds = (self.mediaPlayer.duration())
        self.ui.label_4.setText(self.convert_time(milliseconds))

    def stop(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.stop()
        elif self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.mediaPlayer.stop()

        self.mediaPlayer.setPosition(0)
        self.ui.next.setEnabled(False)
        self.ui.prev.setEnabled(False)

    def prev(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.position = self.position - 5000

            if self.position <= 0:
                self.position = 0

            self.mediaPlayer.setPosition(self.position)
            self.mediaPlayer.play()

    def next(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            duration = self.mediaPlayer.duration()
            self.position += 5000  # 5 secondes
            if self.position >= duration:
                self.position = duration

            self.mediaPlayer.setPosition(self.position)
            self.mediaPlayer.play()

    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)
        self.ui.lbl_vol.setText(str(volume) + "%")

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.play.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.play.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def update_position(self):
        self.ui.slider_position.setValue(self.position)
        self.ui.lbl_temps.setText(self.convert_time(self.position))

    def positionChanged(self, position):
        self.position = position
        self.update_position()
        milliseconds = (self.mediaPlayer.duration())
        self.ui.label_4.setText(self.convert_time(milliseconds))

    def convert_time(self, milliseconds):
        seconds = (int)(milliseconds / 1000) % 60
        minutes = (int)((milliseconds / (1000 * 60)) % 60)
        hours = (int)((milliseconds / (1000 * 60 * 60)) % 24)
        model = "{0:02}:{1:02}:{2:02}"
        model = model.format(hours, minutes, seconds)
        return model

    def durationChanged(self, duration):
        self.ui.slider_position.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        milliseconds = position
        self.ui.lbl_temps.setText(self.convert_time(milliseconds))

    def handleError(self):
        self.ui.play.setEnabled(False)
        if self.mediaPlayer.hasSupport("video/mp4"):
            print("format supporté")

        err = self.mediaPlayer.errorString()
        print(err)

    def on_clicked(self, index):
        pass

    def context_menu(self):
        menu = QMenu()
        open = menu.addAction("Ouvrir")
        open.triggered.connect(self.menu_open)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_video(self):

        rep=self.conf.get_dir_video()

        if not rep:
            rep=QDir.homePath()

        fileName, _ = QFileDialog.getOpenFileName(self, "Ouvrir Vidéos", rep,
                                                  "Fichiers vidéo (*.mp4 *.avi *.mkv)")

        dir = os.path.dirname(fileName)
        if dir:
            self.conf.set_dir_video(dir)

        if fileName == '':
            return

        if os.path.isfile(str(fileName)):
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(str(fileName))))
            self.ui.play.setEnabled(True)

    def open_music(self):

        rep = self.conf.get_dir_video()
        if not rep:
            rep = QDir.homePath()

        fileName, _ = QFileDialog.getOpenFileName(self, "Ouvrir Audio", rep,
                                                  "Fichiers musique (*.mp4 *.mp3 *.wav)")
        dir = os.path.dirname(fileName)
        if dir:
            self.conf.set_dir_music(dir)

        if fileName == '':
            return

        if os.path.isfile(str(fileName)):
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(str(fileName))))
            self.ui.play.setEnabled(True)

    def select_item(self):
        print("selected")

    def close_window(self):
        self.conf.save()
        self.mediaPlayer.stop()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = PlayerScreen()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
