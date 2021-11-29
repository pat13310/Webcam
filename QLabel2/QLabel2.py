from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel, QMenu


class QLabel2(QLabel):
    clicked = pyqtSignal(int, int)
    play = pyqtSignal(int)
    stop = pyqtSignal(int)
    record = pyqtSignal(int)
    capture = pyqtSignal(int)
    link = pyqtSignal(int, int)

    cameras = ["Webcam1", "Webcam2", "Webcam3", "Webcam4", "Ipcam1", "Ipcam2", "Ipcam3", "Ipcam4"]

    def __init__(self, parent=None):
        super(QLabel2, self).__init__(parent)
        self.cam = -1
        self.url = ""
        self.id = 0
        self.device = ""

    def set_default(self):
        self.styleSheet = "QLabel{ color: rgb(255, 255, 255);}\n QLabel:hover{\n border: 1px solid rgb(170, 170, 255);}"
        self.styleMenu = "QMenu{color:white;}\n QMenu::item {background: #a3a3ff ;}\
        QMenu::item:selected {background: #6969ff;}"
        self.setEnabled(True)
        self.setGeometry(QtCore.QRect(140, 290, 640, 480))
        self.setStyleSheet(self.styleSheet)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setScaledContents(True)
        self.blank()

    def blank(self):
        style = "<p align=\"center\"><span style=\" font-size:60pt; color:#6969ff;\">W</span><span style=\" font-size:36pt; color:#a3a3ff;\">ebcam <indice></span></p>"
        style = style.replace("<indice>", str(self.id + 1))
        self.setText(style)

    def mousePressEvent(self, ev):
        self.setStyleSheet("border: 1px  solid  rgb(0, 255, 0)")
        # if ev.button() == QtCore.Qt.LeftButton:
        self.clicked.emit(self.id, self.cam)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setStyleSheet(self.styleSheet)

    def set_assign(self, indice, device):
        self.device = device
        self.cam = indice

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        contextMenu.setStyleSheet(self.styleMenu)
        assignMenu = QMenu(contextMenu)
        assignMenu.setTitle("Assigner")
        startAct = contextMenu.addAction("Démarrer")
        stopAct = contextMenu.addAction("Stop")
        captureAct = contextMenu.addAction("Capture")
        actions = []
        for i in range(8):
            actions.append(assignMenu.addAction(self.cameras[i]))
            actions[i].setCheckable(True)
        contextMenu.addMenu(assignMenu)
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == startAct:
            self.play.emit(self.cam)
        elif action == stopAct:
            # self.blank()
            self.stop.emit(self.cam)
            self.blank()
        elif action == captureAct:
            self.capture.emit(self.cam)
        elif action == actions[0]:
            print("webcam1")
            self.cam = 0
            self.link.emit(self.id, self.cam)
        elif action == actions[1]:
            print("webcam2")
            self.cam = 1
            self.link.emit(self.id, self.cam)
        elif action == actions[2]:
            print("webcam3")
            self.cam = 2
            self.link.emit(self.id, self.cam)
        elif action == actions[3]:
            print("webcam4")
            self.cam = 3
            self.link.emit(self.id, self.cam)
        elif action == actions[4]:
            print("ipcam1")
            self.cam = 4
            self.link.emit(self.id, self.cam)
        elif action == actions[5]:
            print("ipcam2")
            self.cam = 5
            self.link.emit(self.id, self.cam)
        elif action == actions[6]:
            print("ipcam3")
            self.cam = 6
            self.link.emit(self.id, self.cam)
        elif action == actions[7]:
            print("ipcam4")
            self.cam = 7
            self.link.emit(self.id, self.cam)
