import os
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QDir, QUrl, QRectF, QTimer, QPoint
from PyQt5.QtGui import QPainterPath, QRegion, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMenu, QStyle, QFileDialog
import sys

from ConfigApplication.ConfigApplication import ConfigApp
from TimeUtil.horodate import horadate, convert_time
from WebCam import Ui_WebCam
from QSettingMedia import QSettingMedia

from WebCameraCV.WebCamera import WebCamera

class WebScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_WebCam()
        self.ui.setupUi(self)
        self.conf = ConfigApp("web.ini")
        self.setup_gui()
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.play.clicked.connect(self.controlTimer)
        self.ui.stop.clicked.connect(self.controlTimer)
        self.settings=QSettingMedia(self.conf)
        self.camera=WebCamera()

    def setup_gui(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.slider_position.sliderMoved.connect(self.setPosition)

        self.ui.play.setEnabled(True)
        self.ui.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        #self.ui.play.clicked.connect(self.play)

        self.ui.stop.setEnabled(False)
        self.ui.stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        #self.ui.stop.clicked.connect(self.stop)

        self.ui.next.setEnabled(False)
        self.ui.next.clicked.connect(self.next)

        self.ui.prev.setEnabled(False)
        self.ui.prev.clicked.connect(self.prev)

        self.ui.video.clicked.connect(self.open_video)

        self.ui.pushButton_close.clicked.connect(self.close_window)
        self.ui.pushButton_maxi.clicked.connect(self.min_max_window)
        self.ui.chk_adjust.stateChanged.connect(self.adjust) # adjust ratio

        self.ui.picture.clicked.connect(self.capture_picture)

        self.ui.config.clicked.connect(self.show_config)
        self.ratio=False

    def center_cam(self, l, h):
        x=(self.ui.container.width()-l)/2
        y = (self.ui.container.height()-h)/2
        self.ui.screen.move(int(x),int(y))
        self.ui.screen.resize(l,h)

    def min_max_window(self):
        if self.isMaximized():
            self.ui.pushButton_maxi.setText("1")
            self.showNormal()
            if self.camera.is_stop():
                self.ui.screen.setText("<p align=\"center\"><span style=\" font-size:72pt; color:#6969ff;\">W</span><span style=\" font-size:48pt; color:#a3a3ff;\">ebcam</span></p>")
                self.center_cam(self.ui.container.width(),self.ui.container.height())
            else:
                width,height=self.camera.get_dimensions()
                self.center_cam(int(width),int(height))
        else:
            self.ui.pushButton_maxi.setText("2")
            self.showMaximized()
            if self.camera.is_stop():
                self.ui.screen.setText( "<p align=\"center\"><span style=\" font-size:72pt; color:#6969ff;\">W</span><span style=\" font-size:48pt; color:#a3a3ff;\">ebcam</span></p>")

                self.center_cam(self.ui.container.width(), self.ui.container.height())
            else:
                width,height=self.camera.get_dimensions()
                self.center_cam(int(width), int(height))

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


    def show_config(self , conf):
        if self.camera.is_start() :
            self.camera.stop()
            self.ui.stop.setEnabled(True)
            self.ui.play.setEnabled(False)
        self.settings.show()

    # def play(self):
    #     self.state="start"
    #
    # def stop(self):
    #     self.state="stop"

    def prev(self):
        pass

    def next(self):
        pass

    def adjust(self,state):
        if state==QtCore.Qt.Checked:
            self.ratio=True
        else:
            self.ratio = False

    def update_position(self):
        self.ui.slider_position.setValue(self.position)
        self.ui.lbl_duration.setText(convert_time(self.position))

    def positionChanged(self, position):
        self.position = position
        self.update_position()
        milliseconds = (self.mediaPlayer.duration())
        self.ui.lbl_duration.setText(convert_time(milliseconds))

    def capture_picture(self):
        filename=horadate()+".jpg"

        dir=self.conf.get_dir_image()
        if dir=="":
            dir=QDir.homePath()

        path=dir+"/"+filename
        self.camera.capture(path)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        milliseconds = position
        self.ui.lbl_temps.setText(convert_time(milliseconds))

    def handleError(self):
        pass
        err = self.mediaPlayer.errorString()
        print(err)

    def context_menu(self):
        menu = QMenu()
        open = menu.addAction("Ouvrir")
        open.triggered.connect(self.menu_open)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_video(self):
        rep = self.conf.get_dir_video()
        if not rep:
            rep = QDir.homePath()

        fileName, _ = QFileDialog.getOpenFileName(self, "Ouvrir Vidéos", rep, "Fichiers vidéo (*.mp4 *.avi *.mkv)")

        dir = os.path.dirname(fileName)
        if dir:
            self.conf.set_dir_video(dir)

        if fileName == '':
            return

        if os.path.isfile(str(fileName)):
            self.ui.play.setEnabled(True)

    def save_video(self):
        rep = self.conf.get_dir_video()

        if not rep:
            rep = QDir.homePath()

        fileName, _ = QFileDialog.getSaveFileName(self, "Ouvrir Vidéos", rep, "Fichiers vidéo (*.mp4 *.avi *.mkv)")

        dir = os.path.dirname(fileName)
        if dir:
            self.conf.set_dir_video(dir)

        if fileName == '':
            return

    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            self.camera.start()
            width, height=self.camera.get_dimensions()
            self.center_cam(int(width), int(height))
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.play.setEnabled(False)
            self.ui.stop.setEnabled(True)
        # if timer is started
        else:
            self.timer.stop()
            self.camera.stop()
            self.ui.play.setEnabled(True)
            self.ui.stop.setEnabled(False)
            self.ui.screen.setText("<p align=\"center\"><span style=\" font-size:72pt; color:#6969ff;\">W</span><span style=\" font-size:48pt; color:#a3a3ff;\">ebcam</span></p>")

    def viewCam(self):
        if self.camera.is_stop():
            return
        trame=self.camera.update()
        qImg = QImage(trame.image.data, trame.width, trame.height, trame.step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.screen.setPixmap(QPixmap.fromImage(qImg))

    def close_window(self):
        self.conf.save()
        self.camera.stop()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = WebScreen()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
