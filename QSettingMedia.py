import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, QTimer
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsDropShadowEffect
from ConfigApplication.ConfigApplication import ConfigApp
from Settings import Ui_Settings
from WebCameraCV.WebCamThread import WebCameraThread
from WebCameraCV.WebCamera import WebCamera


class QSettingMedia(QMainWindow):

    def __init__(self, conf: ConfigApp):
        QMainWindow.__init__(self)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.conf = conf
        self.cameras = []
        for i in range(8):
            self.cameras.append(WebCameraThread())
            self.cameras[i].indice = i
            if i > 3:
                self.cameras[i].set_url(self.conf.get_url(f"ip{i - 3}"))

            self.cameras[i].image_update.connect(self.on_image)
            self.cameras[i].ready.connect(self.on_dispo)
            self.cameras[i].finished.connect(self.on_finished)
            self.cameras[i].properties_update.connect(self.on_properties)
            self.cameras[i].resolution.connect(self.on_resolution)

        self.desktop = QtWidgets.QDesktopWidget().screenGeometry(0)
        self.setup_gui()
        self.load()
        self.desktop_center()

    def desktop_center(self):
        x = (self.desktop.width() - self.width()) / 2
        y = (self.desktop.height() - self.height()) / 2
        self.move(int(x), 0)

    def setup_gui(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(2)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 190))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        self.ui.pushButton_close.clicked.connect(self.close_window)
        self.ui.pb_cancel.clicked.connect(self.close_window)
        self.ui.pb_apply.clicked.connect(self.apply_window)
        # definir chemins
        self.ui.pb_dir_video.clicked.connect(self.set_dir_video)
        self.ui.pb_dir_image.clicked.connect(self.set_dir_image)
        # sliders
        self.ui.slider_saturation.valueChanged.connect(self.saturation_changed)
        self.ui.slider_contraste.valueChanged.connect(self.contraste_changed)
        self.ui.slider_brillance.valueChanged.connect(self.brillance_changed)
        self.ui.slider_nb_window.valueChanged.connect(self.nb_window_changed)

        self.ui.combo_res.activated[str].connect(self.resolution_changed)

        self.ui.chk_video_horodate.toggled.connect(self.update_video_horodate)
        self.ui.chk_image_horodate.toggled.connect(self.update_image_horodate)

        self.ui.pb_detect_res.clicked.connect(self.auto_detect)

        self.ui.pb_webcam1.clicked.connect(self.on_start_camera)
        self.ui.pb_webcam2.clicked.connect(self.on_start_camera2)
        self.ui.pb_webcam3.clicked.connect(self.on_start_camera3)
        self.ui.pb_webcam4.clicked.connect(self.on_start_camera4)
        self.ui.pb_test_ip1.clicked.connect(self.on_start_camera5)
        self.ui.pb_test_ip2.clicked.connect(self.on_start_camera6)

    def update_video_horodate(self):
        if self.ui.chk_video_horodate.isChecked():
            self.ui.edit_filename_video.setVisible(False)
        else:
            self.ui.edit_filename_video.setVisible(True)

    def update_image_horodate(self):
        if self.ui.chk_image_horodate.isChecked():
            self.ui.edit_filename_image.setVisible(False)
        else:
            self.ui.edit_filename_image.setVisible(True)

    def resolution_changed(self, text):
        self.ui.lbl_res.setText(text)

    def property_changed(self, name, value):
        style = "<p><name>  : <span style=\" color:#aaaaff;\"><value></span></p>"
        style = style.replace("<value>", str(value)).replace("<name>", name)
        return style

    def saturation_changed(self):
        self.ui.lbl_saturation.setText(self.property_changed("Saturation", self.ui.slider_saturation.value()))

    def contraste_changed(self):
        self.ui.lbl_contraste.setText(self.property_changed("Contraste", self.ui.slider_contraste.value()))

    def brillance_changed(self):
        self.ui.lbl_brillance.setText(self.property_changed("Brillance", self.ui.slider_brillance.value()))

    def nb_window_changed(self):
        self.ui.lbl_nb_window.setText(self.property_changed("Fenêtre(s)", self.ui.slider_nb_window.value()))

    def apply_window(self):
        self.conf.set_url("Ip1", self.ui.edit_ip1.text())
        self.conf.set_url("Ip2", self.ui.edit_ip2.text())
        self.conf.set_url("Ip3", self.ui.edit_ip3.text())
        self.conf.set_url("Ip4", self.ui.edit_ip4.text())

        self.conf.set_window("number", str(self.ui.slider_nb_window.value()))
        self.conf.set_window("invert", str(self.ui.chk_inverse.checkState()))
        self.conf.set_horodate("image", str(self.ui.chk_image_horodate.checkState()))
        self.conf.set_horodate("video", str(self.ui.chk_video_horodate.checkState()))

        self.conf.set_image("contraste", str(self.ui.slider_contraste.value()))
        self.conf.set_image("brillance", str(self.ui.slider_brillance.value()))
        self.conf.set_image("saturation", str(self.ui.slider_saturation.value()))
        self.conf.set_image("ratio", str(self.ui.chk_adjust.checkState()))

        self.conf.set_dir_image(self.ui.edit_image.text())
        self.conf.set_dir_video(self.ui.edit_video.text())

        self.conf.set_file_image(self.ui.edit_filename_image.text())
        self.conf.set_file_video(self.ui.edit_filename_video.text())

        self.conf.save()
        self.camera.stop()
        self.camera2.stop()
        self.camera3.stop()
        self.camera4.stop()
        self.close()

    def close_window(self):
        for i in range(8):
            self.cameras[i].stop()
        self.close()

    def load(self):
        if not self.conf:
            return

        self.ui.edit_image.setText(str(self.conf.get_dir_image()))
        self.ui.edit_video.setText(str(self.conf.get_dir_video()))

        self.ui.edit_filename_image.setText(self.conf.get_file_image())
        self.ui.edit_filename_video.setText(self.conf.get_file_video())

        self.ui.edit_ip1.setText(self.conf.get_url("Ip1"))
        self.ui.edit_ip2.setText(self.conf.get_url("Ip2"))
        self.ui.edit_ip3.setText(self.conf.get_url("Ip3"))
        self.ui.edit_ip4.setText(self.conf.get_url("Ip4"))

        v = self.conf.get_window("number")
        if v == "":
            v = "0"
        self.ui.slider_nb_window.setValue(int(v))

        if self.conf.get_window("invert") == '0':
            self.ui.chk_inverse.setChecked(False)
        else:
            self.ui.chk_inverse.setChecked(True)

        if self.conf.get_horodate("image") == '0':
            self.ui.chk_image_horodate.setChecked(False)
        else:
            self.ui.chk_image_horodate.setChecked(True)

        if self.conf.get_horodate("video") == '0':
            self.ui.chk_video_horodate.setChecked(False)
        else:
            self.ui.chk_video_horodate.setChecked(True)

        v = self.conf.get_image("saturation")
        if v == "":
            v = "0"
        self.ui.slider_saturation.setValue(int(v))

        v = self.conf.get_image("contraste")
        if v == "":
            v = "0"
        self.ui.slider_contraste.setValue(int(v))

        self.conf.get_image("brillance")
        if v == "":
            v = "0"
        self.ui.slider_brillance.setValue(int(v))

        if self.conf.get_image("ratio") == '0':
            self.ui.chk_adjust.setChecked(False)
        else:
            self.ui.chk_adjust.setChecked(True)

    def showEvent(self, event):
        # do stuff here
        event.accept()

    def on_dispo(self, disp):
        self.ui.lbl_infos.setText(disp)

    def on_start_camera(self):
        self.start_camera(self.cameras[0], "webcam1")

    def on_start_camera2(self):
        self.start_camera(self.cameras[1], "webcam2")

    def on_start_camera3(self):
        self.start_camera(self.cameras[2], "webcam3")

    def on_start_camera4(self):
        self.start_camera(self.cameras[3], "webcam4")

    def on_start_camera5(self):
        self.camera5.url(self.ui.edit_ip1.text())
        self.start_camera_IP(self.camera5, "webcam5")

    def on_start_camera6(self):
        self.camera6.url(self.ui.edit_ip2.text())
        self.start_camera_IP(self.camera6, "webcam6")

    def start_camera(self, camera, infos):
        if not camera.isRunning():
            camera.start()
        else:
            camera.stop()

    def set_image(self, image, index):
        if index == 1:
            image_scale = image.scaledToHeight(175)
            self.ui.screen.setPixmap(QPixmap.fromImage(image_scale))
        if index == 2:
            image_scale = image.scaledToHeight(110)
            self.ui.screen_2.setPixmap(QPixmap.fromImage(image_scale))
        if index == 3:
            image_scale = image.scaledToHeight(110)
            self.ui.screen_3.setPixmap(QPixmap.fromImage(image_scale))
        if index == 4:
            image_scale = image.scaledToHeight(110)
            self.ui.screen_4.setPixmap(QPixmap.fromImage(image_scale))
        if index == 5:
            image_scale = image.scaledToHeight(110)
            self.ui.screen_3.setPixmap(QPixmap.fromImage(image_scale))
        if index == 6:
            image_scale = image.scaledToHeight(110)
            self.ui.screen_4.setPixmap(QPixmap.fromImage(image_scale))
        if index == 7:
            image_scale = image.scaledToHeight(110)
            self.ui.screen_3.setPixmap(QPixmap.fromImage(image_scale))
        if index == 8:
            image_scale = image.scaledToHeight(110)
            self.ui.screen_4.setPixmap(QPixmap.fromImage(image_scale))

    def on_image(self, image):
        if self.cameras[0] == self.sender():
            if self.cameras[0].isRunning():
                self.set_image(image, 1)
        elif self.sender() == self.cameras[1]:
            if self.cameras[1].isRunning():
                self.set_image(image, 2)
        elif self.sender() == self.cameras[2]:
            if self.cameras[2].isRunning():
                self.set_image(image, 3)
        elif self.sender() == self.cameras[3]:
            if self.cameras[3].isRunning():
                self.set_image(image, 4)
        elif self.sender() == self.cameras[4]:
            if self.cameras[4].isRunning():
                self.set_image(image, 5)
        elif self.sender() == self.cameras[5]:
            if self.cameras[5].isRunning():
                self.set_image(image, 6)
        elif self.sender() == self.cameras[6]:
            if self.cameras[6].isRunning():
                self.set_image(image, 7)
        elif self.sender() == self.cameras[7]:
            if self.cameras[7].isRunning():
                self.set_image(image, 8)

    def auto_detect(self):
        self.cameras[0].auto_detect()

    def on_resolution(self, dict):
        if dict:
            self.ui.combo_res.clear()
            for w, h in dict.items():
                st = w + "x" + h
                self.ui.combo_res.addItem(st)

    def on_finished(self):
        pass

    def on_properties(self, prop):
        pass

    def set_dir_video(self):
        rep = self.conf.get_dir_video()
        if not rep:
            rep = QDir.homePath()

        dir = QFileDialog.getExistingDirectory(self, "Définir chemin Vidéo", rep)
        if dir == '':
            return
        if dir:
            self.ui.edit_video.setText(dir)

    def set_dir_image(self):
        rep = self.conf.get_dir_image()
        if not rep:
            rep = QDir.homePath()

        dir = QFileDialog.getExistingDirectory(self, "Définir chemin Image", rep)
        if dir == '':
            return

        if dir:
            self.ui.edit_image.setText(dir)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = QSettingMedia(None)
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
