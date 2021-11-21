import os

import cv2

VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

RESOLUTIONS={
340:240,
640:480,
800:600,
720:1200,
1440:1080,
}


class WebCamera:

    def __init__(self, index=0):
        self.indice = index
        self.filename_video = ""
        self.filename_image = ""
        self.cap = None
        self.image = None
        self.width = 0
        self.height = 0
        self.state = "stop"
        self.flip = False
        self.recorded = False
        self.inverted=False

    def url(self, url):
        self.indice=url

    def start(self):
        self.cap = cv2.VideoCapture(self.indice, cv2.CAP_DSHOW)
        if self.cap.isOpened():
            self.state = "start"
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            return True
        return False

    def startIP(self):
        self.cap = cv2.VideoCapture(self.indice)
        if self.cap:
            self.state = "start"
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            return True
        return False


    def update(self):

        if self.state=="stop":
            return

        if self.cap:
            ret, self.frame = self.cap.read()

            if ret:
                self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                if self.flip:
                    self.image = cv2.flip(self.image, 1)

                if self.recorded:
                    if self.record_file:
                        self.record_file.write(self.frame)

            height, width, channel = self.image.shape
            step = channel * width
            data = TrameData(self.image, width, height, step)
            return data

    def stop(self):
        self.state = "stop"
        self.recorded = False
        if self.cap:
            self.cap.release()

    def record(self, filename):
        self.filename_video= filename
        self.recorded = True
        size = (self.width, self.height)
        fps=25
        if self.cap:
            self.record_file = cv2.VideoWriter(filename, self.get_video_type(),fps, size)

    def capture(self, path):
        try:
            cv2.imwrite(path, self.image)
        except Exception as err:
            print(err)

    def change_res(self, width, height):
        if self.cap:
            self.cap.set(3, width)
            self.cap.set(4, height)

    def get_video_type(self, filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']

    def get_dimensions(self):
        if self.cap:
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return self.width, self.height

    def set_flip(self, bFlipped):
        self.flip = bFlipped

    def detect_resolution(self):
        if self.cap:
            self.resol={}

            for w,h in RESOLUTIONS.items():
                self.cap.set(3,w)
                self.cap.set(4, h)
                w=int(self.cap.get(3))
                h=int(self.cap.get(4))
                self.resol[str(w)]=str(h)

            return  self.resol

    def is_start(self):
        return  self.state=="start"

    def is_stop(self):
        return  self.state=="stop"

    def properties(self):
        self.test = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        self.ratio = self.cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
        self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.brightness = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        self.contrast = self.cap.get(cv2.CAP_PROP_CONTRAST)
        self.saturation = self.cap.get(cv2.CAP_PROP_SATURATION)
        self.hue = self.cap.get(cv2.CAP_PROP_HUE)
        self.gain = self.cap.get(cv2.CAP_PROP_GAIN)
        self.exposure = self.cap.get(cv2.CAP_PROP_EXPOSURE)

class TrameData:

    def __init__(self, image, width, height, step):
        self.image = image
        self.width = width
        self.height = height
        self.step = step
