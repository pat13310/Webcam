from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

import sys

# GLOBAL


from interface import Ui_Interface


class Interface(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Interface()
        self.ui.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = Interface()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
