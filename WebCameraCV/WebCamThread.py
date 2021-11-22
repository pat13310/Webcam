import os
from datetime import datetime
import time

import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

from WebCameraCV.QCamProperties import QCamProperties

VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

RESOLUTIONS = {
    340: 240,
    640: 480,
    800: 600,
    720: 1200,
    1440: 1080,
}

class WebCameraThread(QThread):
    image_update = pyqtSignal(QImage)
    properties_update = pyqtSignal(QCamProperties)
    finished = pyqtSignal()
    elapsed = pyqtSignal(float)
    dispo=pyqtSignal(str)

    def __init__(self):

        self.indice = 0
        self.filename_video = ""
        self.filename_image = ""
        self.cap = None
        self.record_file=None
        self.state = "no_init"
        self.flip = False
        self.gray = False
        self.recorded = False
        self.inverted = False
        self.ThreadActive = False
        self.snapshot = False
        self.prev_frame_time = 0
        self.mode_ip=False
        self.properties = QCamProperties()
        QtCore.QThread.__init__(self)


    def run(self) -> None:

        self.ThreadActive = True
        fps=0
        if self.mode_ip:
            cap = cv2.VideoCapture(self.indice) # camera ip
            if cap.isOpened():
                self.dispo.emit("disponible")
                cap.set(cv2.CAP_PROP_FPS, float(30))
                fps=cap.get(cv2.CAP_PROP_FPS)
            else:
                self.dispo.emit("indisponible")

        else:
            cap = cv2.VideoCapture(self.indice, cv2.CAP_DSHOW) #webcam
            if cap.isOpened():
                self.dispo.emit("disponible")
                cap.set(cv2.CAP_PROP_FPS, float(30))
                #fps = cap.get(cv2.CAP_PROP_FPS)
            else:
                self.dispo.emit("indisponible")
                cap=None

        if cap:
            self.state = "start"
            self.read_properties(cap)
            self.properties_update.emit(self.properties)
        else:
            self.ThreadActive = False

        while self.ThreadActive:
            self.read_frame(cap)

        if cap:# on libere lesressources
            cap.release()
        self.finished.emit()

        if self.record_file: #on libere pour l'enregistrement
            self.record_file.release()


    def read_frame(self, cap):
        temps1 = time.time()
        ret, self.frame = cap.read()

        if ret:
            self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            height, width, channel = self.image.shape
            step = channel * width
            if self.flip:
                imageflip = cv2.flip(self.image, 1)
                qImg = QImage(imageflip.data, width, height, step, QImage.Format_RGB888)
            else:
                qImg = QImage(self.image.data, width, height, step, QImage.Format_RGB888)

            self.image_update.emit(qImg)

            if self.recorded:
                if self.record_file:
                    self.record_file.write(self.frame)
                    temps2 = time.time()
                    diff = (temps2 - temps1) * 1000
                    self.elapsed.emit(diff)  # millisecond de la video
            else:
                fps = cap.get(cv2.CAP_PROP_FPS)
                if self.mode_ip:
                    fps= fps/10000

                self.elapsed.emit(int(fps))

    def stop(self):
        self.ThreadActive = False
        self.state = "stop"
        self.recorded = False
        self.quit()

    def set_fps(self, fps):
        pass
        #self.cap.set(cv2.CAP_PROP_FPS, fps)
        # self.elapsed.emit()

    def record(self, filename):
        self.filename_video = filename

        size = (int(self.properties.width), int(self.properties.height))
        fps = 10
        if self.isRunning():
            codec = self.get_video_type(filename)
            try:
                self.record_file = cv2.VideoWriter(filename, codec, fps, size)
                self.recorded = True
            except Exception as Err:
                print(Err)

    def capture(self, path):
        self.image_snap = path
        if self.isRunning():
            if self.image_snap:
                cv2.imwrite(self.image_snap, self.frame)

    def get_video_type(self, filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']

    def get_dimensions(self):
        return self.properties.width, self.properties.height

    def set_flip(self, bFlipped):
        self.flip = bFlipped

    def set_gray(self, bGrey):
        self.gray = bGrey
        if self.isRunning():
            if self.gray:
                self.cap.set(12, 2)
            else:
                self.cap.set(12, 50)


    def set_property(self, property_id, value):
        if self.isRunning():
            self.cap.set(property_id, value)

    def detect_resolution(self):
        if self.cap:
            self.resol = {}

            for w, h in RESOLUTIONS.items():
                self.cap.set(3, w)
                self.cap.set(4, h)
                w = int(self.cap.get(3))
                h = int(self.cap.get(4))
                self.resol[str(w)] = str(h)

            return self.resol

    def read_properties(self, cap):
        self.cap = cap
        # self.reset_properties()
        self.properties.test = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        self.properties.ratio = self.cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
        self.properties.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
        self.properties.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.properties.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.properties.brightness = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        self.properties.contrast = self.cap.get(cv2.CAP_PROP_CONTRAST)
        self.properties.saturation = self.cap.get(cv2.CAP_PROP_SATURATION)
        self.properties.hue = self.cap.get(cv2.CAP_PROP_HUE)
        self.properties.gain = self.cap.get(cv2.CAP_PROP_GAIN)
        self.properties.exposure = self.cap.get(cv2.CAP_PROP_EXPOSURE)

    def reset_properties(self):
        if self.isRunning():
            self.cap.set(cv2.CAP_PROP_SETTINGS, 0)

    def set_url(self, url):
        self.indice=url

    def set_mode_ip(self, mode):
        self.mode_ip=mode

    def set_name(self, name):
        self.name=name

    # self.read_properties(self.cap)
