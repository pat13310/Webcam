import os
import time

import cv2
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QDir, QTimer, QCoreApplication, QElapsedTimer
from PyQt5.QtGui import QPainterPath, QRegion, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMenu, QStyle, QFileDialog
import sys
from ConfigApplication.ConfigApplication import ConfigApp
from TimeUtil.horodate import horadate, convert_time
from WebCam import Ui_WebCam
from QSettingMedia import QSettingMedia
from WebCameraCV.QCamProperties import QCamProperties
from WebCameraCV.WebCamThread import WebCameraThread


class WebScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_WebCam()
        self.timer: QTimer = QTimer()
        self.timer2 = QElapsedTimer()
        self.ui.setupUi(self)
        self.conf = ConfigApp("web.ini")
        self.properties: QCamProperties = None
        self.setup_gui()
        # set control_bt callback clicked  function
        self.ui.play.clicked.connect(self.play)
        self.ui.stop.clicked.connect(self.stop)
        self.ui.record.clicked.connect(self.record)
        self.settings = QSettingMedia(self.conf)
        self.cameras = []
        self.camera = None

        for i in range(4):
            self.cameras.append(WebCameraThread())
            self.cameras[i].set_name(f"webcam{i + 1}")
            self.setup_camera(self.cameras[i])
            self.cameras[i].indice = i

        for i in range(4, 8):
            self.cameras.append(WebCameraThread())
            self.cameras[i].set_name(f"ipcam{i - 3}")
            self.setup_camera(self.cameras[i])
            self.cameras[i].set_mode_ip(True)
            self.cameras[i].set_url(self.conf.get_url(f"ip{i - 3}"))

        self.ui.comboCamera.activated[str].connect(self.on_change_camera)
        self.init_camera()
        self.camera = self.cameras[0]

    def setup_camera(self, cam):
        cam.image_update.connect(self.image_update)
        cam.properties_update.connect(self.properties_update)
        cam.finished.connect(self.on_stop)
        cam.elapsed.connect(self.on_elapsed)
        cam.dispo.connect(self.on_infos)

    def init_camera(self):
        self.ui.comboCamera.clear()

        for i in range(8):
            self.ui.comboCamera.addItem(self.cameras[i].name)
            if self.cameras[i].mode_ip:
                self.conf.set_camera(f"webcam{i + 1}", str(self.cameras[i].indice))
            else:
                self.conf.set_camera(self.cameras[i].name, str(i))

    def detect_camera(self):
        self.ui.comboCamera.clear()
        for i in range(1, 4):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.ui.comboCamera.addItem(f"webcam{i + 1}", userData=i)
                self.conf.set_camera(f"webcam{i + 1}", str(i))

    def on_change_camera(self, text):
        if self.camera:
            if self.camera.isRunning:
                self.stop()
            self.camera = None

        index = self.ui.comboCamera.currentIndex()
        self.ui.label_infos.setText("Détection en cours ...")
        self.ui.play.setEnabled(False)
        self.ui.stop.setEnabled(False)
        self.ui.record.setEnabled(False)
        self.ui.split.setEnabled(False)
        self.camera = self.cameras[index]
        self.play()

    def on_infos(self, text):
        if text == "indisponible":
            self.ui.led.setPixmap(QtGui.QPixmap(":/icones/icones/media/led_rouge.png"))
            self.ui.play.setEnabled(False)
            self.ui.stop.setEnabled(False)
            self.ui.record.setEnabled(False)
            self.ui.split.setEnabled(False)
            self.ui.slider_saturation.setValue(0)
            self.ui.slider_brillance.setValue(0)
            self.ui.slider_contraste.setValue(0)
        if text == 'disponible':
            self.ui.led.setPixmap(QtGui.QPixmap(":/icones/icones/media/led_verte.png"))
            self.ui.record.setEnabled(True)
            self.ui.split.setEnabled(True)

        self.ui.label_infos.setText(text)

    def on_elapsed(self, milli):
        if self.camera.recorded:
            self.ui.lbl_duration.setText(convert_time(milli))
        else:
            self.ui.lbl_duration.setText(str(milli) + " fps")

    def properties_update(self, properties):
        self.properties = properties
        self.ui.slider_saturation.setValue(int(self.properties.saturation))
        self.ui.slider_brillance.setValue(int(self.properties.brightness))
        self.ui.slider_contraste.setValue(int(self.properties.contrast))
        self.center_cam(self.properties.width, self.properties.height)

    def image_update(self, image):
        if self.camera.isRunning():
            self.ui.screen.setPixmap(QPixmap.fromImage(image))

    def center_cam(self, l, h):
        x = (self.ui.container.width() - l) / 2
        y = (self.ui.container.height() - h) / 2
        self.ui.screen.move(int(x), int(y))
        self.ui.screen.resize(int(l), int(h))

    def setup_gui(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.play.setEnabled(True)
        self.ui.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.stop.setEnabled(False)
        self.ui.stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.ui.split.setEnabled(False)

        self.ui.pushButton_close.clicked.connect(self.close_window)
        self.ui.pushButton_maxi.clicked.connect(self.min_max_window)
        self.ui.chk_adjust.stateChanged.connect(self.adjust)  # adjust ratio

        self.ui.video.clicked.connect(self.open_video)
        self.ui.picture.clicked.connect(self.capture_picture)
        self.ui.config.clicked.connect(self.show_config)

        self.ui.chk_adjust.toggled.connect(self.adjust)
        self.ui.chk_inverse.toggled.connect(self.flip)
        self.ui.chk_grey.toggled.connect(self.grey)

        self.ui.slider_contraste.valueChanged.connect(self.on_contraste)
        self.ui.slider_brillance.valueChanged.connect(self.on_brillance)
        self.ui.slider_saturation.valueChanged.connect(self.on_saturation)
        self.ratio = False
        self.timer.timeout.connect(self.on_timer)

    def set_infos(self, text):
        self.infos_screen = text
        style = "<p align=\"center\"><span style=\" font-size:22pt; font-style:italic; color:#aaaaff;\"><texte></span></p>"
        style = style.replace("<texte>", text)
        self.timer.start(20)
        self.timer2.start()
        self.ui.lbl_screen.setText(style)

    def on_timer(self):
        self.ui.lbl_screen.setText(self.infos_screen)
        self.timer.stop()

        while self.timer2.elapsed()<1100:
            QCoreApplication.processEvents()

        self.ui.lbl_screen.setText("")

    def min_max_window(self):
        if self.isMaximized():
            self.ui.pushButton_maxi.setText("1")
            self.showNormal()
            if self.camera.isFinished():
                self.ui.screen.setText(
                    "<p align=\"center\"><span style=\" font-size:72pt; color:#6969ff;\">W</span><span style=\" font-size:48pt; color:#a3a3ff;\">ebcam</span></p>")
                self.center_cam(self.ui.container.width(), self.ui.container.height())
            else:
                width, height = self.camera.get_dimensions()
                self.center_cam(int(width), int(height))
        else:
            self.ui.pushButton_maxi.setText("2")
            self.showMaximized()
            if self.camera.isFinished():
                self.ui.screen.setText(
                    "<p align=\"center\"><span style=\" font-size:72pt; color:#6969ff;\">W</span><span style=\" font-size:48pt; color:#a3a3ff;\">ebcam</span></p>")

                self.center_cam(self.ui.container.width(), self.ui.container.height())
            else:
                width, height = self.camera.get_dimensions()
                self.center_cam(int(width), int(height))

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

    def show_config(self, conf):
        if self.camera:
            if self.camera.isRunning():
                self.camera.stop()
                self.ui.stop.setEnabled(False)
                self.ui.play.setEnabled(True)
        self.settings.show()

    def play(self):
        self.ui.play.setEnabled(False)
        self.ui.stop.setEnabled(True)
        if self.camera:
            self.camera.start()
            self.set_infos("Démarrage")

    def stop(self):
        self.ui.led.setPixmap(QtGui.QPixmap(":/icones/icones/media/led_rouge.png"))
        self.ui.play.setEnabled(True)
        self.ui.stop.setEnabled(False)
        self.ui.record.setEnabled(True)
        self.ui.split.setEnabled(False)
        if self.camera:
            self.camera.stop()
            self.set_infos("Stop")

    def record(self):
        if self.camera:
            if self.conf.get_horodate("video") == "0":
                path = self.conf.get_dir_video() + "/" + self.conf.get_file_video()
            else:
                path = self.conf.get_dir_video() + "/" + horadate() + ".avi"
            self.ui.led.setPixmap(QtGui.QPixmap(":/icones/icones/media/led_orange.png"))
            self.camera.record(path)
            self.ui.play.setEnabled(False)
            self.ui.record.setEnabled(False)
            self.set_infos("Enregistrement en cours ...")

    def on_stop(self):  # vient du thread
        self.blank_screen()

    def flip(self):
        if self.camera:
            if self.camera.isRunning():
                if self.ui.chk_inverse.isChecked():
                    self.camera.set_flip(True)
                    self.set_infos("Mode Inversé")
                else:
                    self.camera.set_flip(False)
                    self.set_infos("Mode Normal")

    def grey(self):
        if self.camera:
            if self.camera.isRunning():
                if self.ui.chk_grey.isChecked():
                    self.camera.set_gray(True)
                    self.ui.slider_saturation.setValue(2)
                    self.conf.set_image("saturation", "2")

                    self.set_infos("Mode Gris")
                else:
                    self.camera.set_gray(False)
                    self.ui.slider_saturation.setValue(50)
                    self.conf.set_image("saturation", "50")
                    self.set_infos("Mode Couleur")

    def property_changed(self, name, value):
        style = "<p><name>  : <span style=\" color:#aaaaff;\"><value></span></p>"
        style = style.replace("<value>", str(value)).replace("<name>", name)
        return style

    def adjust(self, state):
        if state == QtCore.Qt.Checked:
            self.ratio = True
        else:
            self.ratio = False

    def on_contraste(self):
        if self.camera:
            self.camera.set_property(11, float(self.ui.slider_contraste.value()))
            self.ui.lbl_contraste.setText(self.property_changed("Contraste", self.ui.slider_contraste.value()))

    def on_brillance(self):
        if self.camera:
            self.camera.set_property(10, float(self.ui.slider_brillance.value()))
            self.ui.lbl_brillance.setText(self.property_changed("Brillance", self.ui.slider_brillance.value()))

    def on_saturation(self):
        if self.camera:
            self.camera.set_property(12, float(self.ui.slider_saturation.value()))
            self.ui.lbl_saturation.setText(self.property_changed("Saturation", self.ui.slider_saturation.value()))

    def update_position(self):
        self.ui.slider_position.setValue(self.position)
        self.ui.lbl_duration.setText(convert_time(self.position))

    def capture_picture(self):
        filename = horadate() + ".jpg"
        dir = self.conf.get_dir_image()
        if dir == "":
            dir = QDir.homePath()
        path = dir + "/" + filename
        if self.camera:
            self.camera.capture(path)
            self.set_infos("Capture écran")

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

    def blank_screen(self):
        self.ui.screen.setText(
            "<p align=\"center\"><span style=\" font-size:72pt; color:#6969ff;\">W</span><span style=\" font-size:48pt; color:#a3a3ff;\">ebcam</span></p>")

    def close_window(self):
        self.conf.save()
        if self.camera:
            self.camera.stop()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = WebScreen()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
