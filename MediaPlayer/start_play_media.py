import os.path

from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import sys

class VideoPlayer:

    def __init__(self):

        self.video = QVideoWidget()
        self.video.resize(600, 400)
        self.video.move(0, 0)

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video)

        if os.path.isfile("D:/Musique/test.mp4"):
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(r"D:/Musique/test.mp4")))
        else:
            print ("pas de fichier")

    def callback(self):
        self.player.setPosition(0) # to start at the beginning of the video every time
        self.video.show()
        self.player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = VideoPlayer()
    b = QPushButton('start')
    b.clicked.connect(v.callback)
    b.show()
    sys.exit(app.exec_())