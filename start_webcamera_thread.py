import os

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QDir, QTimer, QCoreApplication, QElapsedTimer
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QStyle, QFileDialog, QLabel, QGraphicsDropShadowEffect
import sys
from ConfigApplication.ConfigApplication import ConfigApp
from QLabel2.QLabel2 import QLabel2

from TimeUtil.horodate import horadate, convert_time
from WebCam import Ui_WebCam
from QSettingMedia import QSettingMedia
from WebCameraCV.QCamProperties import QCamProperties
from WebCameraCV.WebCamThread import WebCameraThread


def property_changed(name, value):
    style = "<p><name>  : <span style=\" color:#aaaaff;\"><value></span></p>"
    style = style.replace("<value>", str(value)).replace("<name>", name)
    return style


class WebScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.ui = Ui_WebCam()
        self.ui.setupUi(self)
        self.ratio = False
        self.timer: QTimer = QTimer()
        self.timer2 = QElapsedTimer()
        self.active_index = 0
        self.infos_screen = ""
        self.properties = None
        self.screens = []
        for i in range(4):
            self.screens.append(QLabel2(self.ui.container))
            self.screens[i].setObjectName(f"screen{i + 1}")
            self.screens[i].id = i
            self.screens[i].set_default()
            self.screens[i].clicked.connect(self.on_select_screen)
            self.screens[i].play.connect(self.on_play)
            self.screens[i].stop.connect(self.on_stop)
            self.screens[i].record.connect(self.on_record)
            self.screens[i].link.connect(self.on_link)
            self.screens[i].capture.connect(self.capture_picture)

        self.setup_gui()
        self.conf = ConfigApp("web.ini")
        self.properties: QCamProperties

        self.ui.play.clicked.connect(self.play)
        self.ui.stop.clicked.connect(self.stop)
        self.ui.record.clicked.connect(self.record)
        self.settings = QSettingMedia(self.conf)
        self.cameras = []
        self.camera = None
        self.nb_window = 1

        for i in range(8):
            self.cameras.append(WebCameraThread())
            if i > 3:
                self.cameras[i].set_url(self.conf.get_url(f"ip{i - 3}"))
                self.cameras[i].set_indice(i - 3)
            else:
                self.cameras[i].set_indice(i)

            self.cameras[i].image_update.connect(self.on_image)
            self.cameras[i].properties_update.connect(self.properties_update)
            self.cameras[i].finished.connect(self.on_thread_stop)
            self.cameras[i].elapsed.connect(self.on_elapsed)
            self.cameras[i].ready.connect(self.on_ready)

        self.ui.comboCamera.activated[str].connect(self.on_change_camera)
        self.combo_camera()
        self.camera = self.cameras[0]

        self.desktop = QtWidgets.QDesktopWidget().screenGeometry(0)
        self.desktop_center()
        self.offset = None
        lw = 400
        h = 100
        x = (800 - lw) / 2
        y = (500 - h) / 2
        self.screens[self.active_index].move(int(x), int(y))
        self.screens[self.active_index].resize(int(lw), int(h))
        self.screens[self.active_index].cam = 0

    def desktop_center(self):
        x = (self.desktop.width() - self.width()) / 2
        y = (self.desktop.height() - self.height()) / 2
        self.move(int(x), int(y) - 20)

    def on_select_screen(self, indice, camera):
        print(f"clicked label:{indice} camera:{camera}")
        self.active_index = indice
        self.camera = self.cameras[camera]
        self.cameras[camera].set_label(indice)

    def combo_camera(self):
        self.ui.comboCamera.clear()
        for i in range(8):
            self.ui.comboCamera.addItem(self.cameras[i].name)
            if self.cameras[i].mode_ip:
                self.conf.set_camera(f"webcam{i + 1}", str(self.cameras[i].indice))
            else:
                self.conf.set_camera(self.cameras[i].name, str(i))

    def on_change_camera(self, text):
        print(text)
        if self.camera:
            if self.camera.isRunning:
                if self.nb_window == 1:
                    self.stop()
                self.camera = None

        index = self.ui.comboCamera.currentIndex()
        self.ui.play.setEnabled(False)
        self.ui.stop.setEnabled(False)
        self.ui.record.setEnabled(False)
        self.ui.split.setEnabled(True)
        self.camera = self.cameras[index]
        self.play()

    def on_ready(self, text):
        if "indisponible" in text:
            self.ui.led.setPixmap(QtGui.QPixmap(":/icones/icones/media/led_rouge.png"))
            self.ui.play.setEnabled(False)
            self.ui.stop.setEnabled(False)
            self.ui.record.setEnabled(False)
            self.ui.split.setEnabled(True)
            self.ui.slider_saturation.setValue(0)
            self.ui.slider_brillance.setValue(0)
            self.ui.slider_contraste.setValue(0)
            return
        if "disponible" in text:
            self.ui.led.setPixmap(QtGui.QPixmap(":/icones/icones/media/led_verte.png"))
            self.ui.record.setEnabled(True)
            self.ui.split.setEnabled(True)

    def on_elapsed(self, milli):
        if self.camera.isRunning():
            if self.camera.recorded:
                self.ui.lbl_duration.setText(convert_time(milli))
            else:
                self.ui.lbl_duration.setText(str(milli) + " fps")

    def properties_update(self, properties):
        self.properties = properties
        self.ui.slider_saturation.setValue(int(self.properties.saturation))
        self.ui.slider_brillance.setValue(int(self.properties.brightness))
        self.ui.slider_contraste.setValue(int(self.properties.contrast))

    def on_image(self, image, screen, camera):
        if self.cameras[camera].isRunning():
            self.screens[screen].setPixmap(QPixmap.fromImage(image))

    def center_cam(self, lw, h):
        # lw = self.ui.container.width()
        # hw = self.ui.container.height()
        x = (self.ui.container.width() - lw) / 2
        y = (self.ui.container.height() - h) / 2
        self.screens[self.active_index].move(int(x), int(y))
        self.screens[self.active_index].resize(int(lw), int(h))

    def center_label(self, lw, h, label: QLabel):
        x = (self.ui.container.width() - lw) / 2
        y = (self.ui.container.height() - 55)
        label.move(int(x), int(y))
        label.resize(int(lw), int(h))

    def setup_gui(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(3)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 190))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        self.ui.play.setEnabled(True)
        self.ui.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.stop.setEnabled(False)
        self.ui.stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.ui.split.setEnabled(True)
        self.ui.record.setEnabled(False)

        self.ui.pushButton_close.clicked.connect(self.close_window)
        self.ui.pushButton_maxi.clicked.connect(self.min_max_window)

        self.ui.video.clicked.connect(self.open_video)
        self.ui.picture.clicked.connect(self.capture_picture)
        self.ui.config.clicked.connect(self.show_config)

        self.ui.chk_adjust.toggled.connect(self.on_adjust)
        self.ui.chk_inverse.toggled.connect(self.flip)
        self.ui.chk_grey.toggled.connect(self.grey)

        self.ui.slider_contraste.valueChanged.connect(self.on_contraste)
        self.ui.slider_brillance.valueChanged.connect(self.on_brillance)
        self.ui.slider_saturation.valueChanged.connect(self.on_saturation)
        self.timer.timeout.connect(self.on_timer)
        self.ui.split.clicked.connect(self.on_split)
        self.screens[1].setVisible(False)
        self.screens[2].setVisible(False)
        self.screens[3].setVisible(False)

    def on_window(self, nb):
        if nb == 1:
            self.screens[1].setVisible(False)
            self.screens[2].setVisible(False)
            self.screens[3].setVisible(False)
            if self.isMaximized():
                if self.ratio:
                    h = self.ui.container.height() - 10
                    lw = 1.33333333333 * h
                else:
                    lw = 640
                    h = lw * 0.75
            else:
                self.resize(self.desktop.width() - 220, self.desktop.height() - 120)
                if self.ratio:
                    lw = self.ui.container.width() - 10
                    h = lw * 0.75
                else:
                    lw = 640
                    h = lw * 0.75
            self.center_cam(lw, h)

        elif nb == 2:
            self.screens[1].setVisible(True)
            self.screens[2].setVisible(False)
            self.screens[3].setVisible(False)
            marge = 15
            if self.isMaximized():
                lw = self.ui.container.width()
                hw = self.ui.container.height()
                if self.ratio:
                    w = lw / 2 - marge
                    h = w * 0.75
                    x = (lw - w * 2) / 2
                    y = (hw - h) / 2
                else:
                    w = 440
                    h = w * 0.75
                    x = (lw - 2 * w) / 2
                    y = (hw - h) / 2

            else:  # normal screen
                lw = self.ui.container.width()
                hw = self.ui.container.height()
                if self.ratio:
                    w = lw / 2 - marge
                    h = w * 0.75
                    x = (lw - w * 2) / 2
                    y = (hw - h) / 2
                else:
                    w = 520
                    h = w * 0.75
                    self.resize(self.desktop.width() - 10, self.desktop.height() - 120)
                    lw = self.ui.container.width()
                    hw = self.ui.container.height()
                    x = (lw - w * 2) / 2
                    y = (hw - h) / 2

            self.screens[0].move(int(x), int(y))
            self.screens[0].resize(int(w), int(h))
            self.screens[1].move(int(x + w) + 5, int(y))
            self.screens[1].resize(int(w), int(h))

        elif nb == 4:
            self.screens[1].setVisible(True)
            self.screens[2].setVisible(True)
            self.screens[3].setVisible(True)

            if self.isMaximized():
                if self.ratio:
                    lw = self.ui.container.width() - 2
                    h = self.ui.container.height() - 2
                    largeur = (h * 1.33333333333) / 2
                    hauteur = h / 2
                    x = (lw - largeur * 2) / 2
                    y = (h - hauteur * 2) / 2
                    espace = 4
                else:
                    lw = self.ui.container.width() - 5
                    h = self.ui.container.height() - 5
                    largeur = 400
                    hauteur = largeur * 0.75
                    x = (lw - largeur * 2) / 2
                    y = (h - hauteur * 2) / 2
                    espace = 4

            else:  # normal
                self.resize(self.desktop.width() - 15, self.desktop.height() - 72)
                if self.ratio:
                    lw = self.ui.container.width() - 5
                    h = self.ui.container.height() - 5
                    largeur = (h * 1.33333333333) / 2
                    hauteur = h / 2
                    x = ((lw - largeur * 2) / 2)
                    y = ((h - hauteur * 2) / 2)
                    espace = 4
                else:
                    lw = self.ui.container.width() - 5
                    hw = self.ui.container.height() - 5
                    largeur = 340
                    hauteur = largeur * 0.75
                    x = (lw - largeur * 2) / 2
                    y = ((hw - hauteur * 2) / 2)
                    espace = 20

            self.screens[0].move(int(x), int(y))
            self.screens[0].resize(int(largeur), int(hauteur))
            self.screens[1].move(int(x + largeur + espace), int(y))
            self.screens[1].resize(int(largeur), int(hauteur))
            self.screens[2].move(int(x), int(y + hauteur + espace))
            self.screens[2].resize(int(largeur), int(hauteur))
            self.screens[3].move(int(x + largeur + espace), int(y + hauteur + espace))
            self.screens[3].resize(int(largeur), int(hauteur))

        if not self.isMaximized():
            self.desktop_center()

    def on_split(self):
        if self.nb_window == 1:
            self.nb_window = 2
            self.on_window(self.nb_window)

        elif self.nb_window == 2:
            self.nb_window = 4
            self.on_window(self.nb_window)

        elif self.nb_window == 4:
            self.nb_window = 1
            self.on_window(self.nb_window)

    def set_infos(self, text):
        self.infos_screen = text
        style = "<p align=\"center\"><span style=\"font-size:12pt;/" \
                "font-style:italic; color:#aaaaff;\"><texte></span></p>"
        style = style.replace("<texte>", text)
        self.timer.start(20)
        self.timer2.start()
        self.ui.lbl_screen.raise_()
        self.ui.lbl_screen.setText(style)
        self.center_label(200, 80, self.ui.lbl_screen)

    def on_timer(self):
        self.timer.stop()
        while self.timer2.elapsed() < 1100:
            QCoreApplication.processEvents()
        self.ui.lbl_screen.setText("")

    def min_max_window(self):
        if self.isMaximized():
            self.ui.pushButton_maxi.setText("1")
            self.showNormal()
            if self.camera.isFinished():
                if self.screens[self.active_index]:
                    self.screens[self.active_index].blank()
                    self.center_cam(self.ui.container.width(), self.ui.container.height())
            else:
                self.on_window(self.nb_window)
        else:
            self.ui.pushButton_maxi.setText("2")
            self.showMaximized()
            if self.camera.isFinished():
                if self.screens[self.active_index]:
                    self.screens[self.active_index].blank()
                    self.center_cam(self.ui.container.width(), self.ui.container.height())
            else:
                self.on_window(self.nb_window)

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

    def show_config(self):
        if self.camera:
            if self.camera.isRunning():
                self.camera.stop()
                self.ui.stop.setEnabled(False)
                self.ui.play.setEnabled(True)
        self.settings.show()

    def showEvent(self, event):
        # do stuff here
        self.on_window(self.nb_window)
        event.accept()

    def on_play(self, index):
        self.camera = self.cameras[index]
        self.play()

    def play(self):
        self.ui.play.setEnabled(False)
        self.ui.stop.setEnabled(True)
        self.ui.record.setEnabled(True)
        self.on_window(self.nb_window)
        if self.camera:
            self.camera.start()
            self.set_infos("Démarrage")

    def on_stop(self, index):
        self.camera = self.cameras[index]
        self.stop()

    def stop(self):
        self.ui.led.setPixmap(QtGui.QPixmap(":/icones/icones/media/led_rouge.png"))
        self.ui.play.setEnabled(True)
        self.ui.stop.setEnabled(False)
        self.ui.record.setEnabled(False)
        self.ui.split.setEnabled(True)
        if self.camera:
            self.camera.stop()
            self.set_infos("Stop")

    def on_record(self, index):
        self.camera = self.cameras[index]
        self.record()

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

    def on_link(self, screen_id, index):
        self.camera = self.cameras[index]
        self.camera.set_label(screen_id)

    def on_thread_stop(self):  # vient du thread
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

    def center_infos(self):
        lw = self.ui.lbl_screen.width()
        # h = self.ui.lbl_screen.height()
        lc = self.ui.container.width()
        hc = self.ui.container.height()
        x = (lc - lw)
        y = hc - 150
        self.ui.lbl_screen.move(int(x), int(y))

    def on_adjust(self, state):
        if state:
            self.ratio = True
            self.on_window(self.nb_window)

            self.set_infos("Ajusté à l'écran")
        else:
            self.ratio = False
            self.on_window(self.nb_window)

            self.set_infos("Taille réelle")

    def on_contraste(self):
        if self.camera:
            self.camera.set_property(11, float(self.ui.slider_contraste.value()))
            self.ui.lbl_contraste.setText(property_changed("Contraste", self.ui.slider_contraste.value()))
            # self.set_infos("Contraste")

    def on_brillance(self):
        if self.camera:
            self.camera.set_property(10, float(self.ui.slider_brillance.value()))
            self.ui.lbl_brillance.setText(property_changed("Brillance", self.ui.slider_brillance.value()))
            # self.set_infos("Brillance")

    def on_saturation(self):
        if self.camera:
            self.camera.set_property(12, float(self.ui.slider_saturation.value()))
            self.ui.lbl_saturation.setText(property_changed("Saturation", self.ui.slider_saturation.value()))
            # self.set_infos("Saturation")

    def update_position(self):
        self.ui.slider_position.setValue(self.position)
        self.ui.lbl_duration.setText(convert_time(self.position))

    def capture_picture(self):
        filename = horadate() + ".jpg"
        directory = self.conf.get_dir_image()
        if directory == "":
            directory = QDir.homePath()
        path = directory + "/" + filename
        if self.camera:
            self.camera.capture(path)
            self.set_infos("Capture écran")

    # def contextMenuEvent(self, event):
    #     contextMenu = QMenu(self)
    #     assignMenu = QMenu(contextMenu)
    #     assignMenu.setTitle("Assigner")
    #     startAct = contextMenu.addAction("Démarrer")
    #     stopAct = contextMenu.addAction("Stop")
    #     captureAct = contextMenu.addAction("Capture")
    #     actions = []
    #     for i in range(8):
    #         actions.append(assignMenu.addAction(self.cameras[i].name))
    #         actions[i].setCheckable(True)
    #     contextMenu.addMenu(assignMenu)
    #
    #     if self.camera.isRunning():
    #         startAct.setEnabled(False)
    #         stopAct.setEnabled(True)
    #         captureAct.setEnabled(True)
    #     else:
    #         startAct.setEnabled(True)
    #         stopAct.setEnabled(False)
    #         captureAct.setEnabled(False)
    #
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    #     if action == startAct:
    #         self.play()
    #     elif action == stopAct:
    #         self.stop()
    #     elif action == captureAct:
    #         self.capture_picture()
    #     elif action == actions[0]:
    #         print("webcam1")
    #         self.cameras[0].set_label(self.screens[self.active_index].id)
    #         self.screens[self.active_index].camera = 0
    #         self.camera = self.cameras[0]
    #     elif action == actions[1]:
    #         print("webcam2")
    #         self.cameras[1].set_label(self.screens[self.active_index].id)
    #         self.camera = self.cameras[1]
    #         self.screens[self.active_index].camera = 1

    def open_video(self):
        rep = self.conf.get_dir_video()
        if not rep:
            rep = QDir.homePath()
        filename, _ = QFileDialog.getOpenFileName(self, "Ouvrir Vidéos", rep, "Fichiers vidéo (*.mp4 *.avi *.mkv)")
        directory = os.path.dirname(filename)
        if directory:
            self.conf.set_dir_video(directory)
        if filename == '':
            return

        if os.path.isfile(str(filename)):
            self.ui.play.setEnabled(True)

    def save_video(self):
        rep = self.conf.get_dir_video()
        if not rep:
            rep = QDir.homePath()
        filename, _ = QFileDialog.getSaveFileName(self, "Ouvrir Vidéos", rep, "Fichiers vidéo (*.mp4 *.avi *.mkv)")
        directory = os.path.dirname(filename)
        if directory:
            self.conf.set_dir_video(directory)
        if filename == '':
            return

    def blank_screen(self):
        self.screens[self.active_index].blank()

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
