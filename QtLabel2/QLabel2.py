from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel


class QLabel2(QLabel):
    clicked = pyqtSignal(int)

    def __init(self, parent):
        QLabel.__init__(self, QMouseEvent)
        self.indice = 1

    def set_default(self):
        self.setEnabled(True)
        self.setGeometry(QtCore.QRect(140, 290, 600, 180))
        self.style="QLabel{ color: rgb(255, 255, 255);}\n QLabel:hover{\n border: 1px solid rgb(170, 170, 255);}\n"


        self.setStyleSheet(self.style)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setScaledContents(True)
        self.blank()

    def blank(self):
        style = "<html><head/><body><p align=\"center\"><span style=\" font-size:72pt; color:#6969ff;\">W</span><span style=\" font-size:48pt; color:#a3a3ff;\">ebcam <indice></span></p></body></html>"
        style = style.replace("<indice>", str(self.indice))
        self.setText(style)

    def mousePressEvent(self, ev):
        self.setStyleSheet("border: 1px  solid  rgb(0, 255, 0)")
        self.clicked.emit(self.indice)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setStyleSheet(self.style)
