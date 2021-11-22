# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Interface(object):
    def setupUi(self, Interface):
        Interface.setObjectName("Interface")
        Interface.resize(980, 524)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        Interface.setPalette(palette)
        Interface.setStyleSheet("\n"
"")
        self.centralwidget = QtWidgets.QWidget(Interface)
        self.centralwidget.setObjectName("centralwidget")
        Interface.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(Interface)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 980, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFichier = QtWidgets.QMenu(self.menuBar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuR_cents = QtWidgets.QMenu(self.menuFichier)
        self.menuR_cents.setObjectName("menuR_cents")
        self.menuEdition = QtWidgets.QMenu(self.menuBar)
        self.menuEdition.setObjectName("menuEdition")
        self.menuForm = QtWidgets.QMenu(self.menuBar)
        self.menuForm.setObjectName("menuForm")
        self.menuVue = QtWidgets.QMenu(self.menuBar)
        self.menuVue.setObjectName("menuVue")
        self.menuConfig = QtWidgets.QMenu(self.menuBar)
        self.menuConfig.setObjectName("menuConfig")
        self.menuFen_tre = QtWidgets.QMenu(self.menuBar)
        self.menuFen_tre.setObjectName("menuFen_tre")
        self.menuAide = QtWidgets.QMenu(self.menuBar)
        self.menuAide.setObjectName("menuAide")
        Interface.setMenuBar(self.menuBar)
        self.toolBar = QtWidgets.QToolBar(Interface)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 40))
        self.toolBar.setObjectName("toolBar")
        Interface.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QtWidgets.QDockWidget(Interface)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.dockWidgetContents)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolBox = QtWidgets.QToolBox(self.widget)
        self.toolBox.setStyleSheet("color: rgb(85, 170, 255);\n"
"background-color: rgb(227, 227, 227);\n"
"border-color:rgb(85, 85, 255);\n"
"selection-color: rgb(85, 170, 255);\n"
"border-radius:10px 0px 0px 10px ;")
        self.toolBox.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox.setLineWidth(1)
        self.toolBox.setObjectName("toolBox")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setGeometry(QtCore.QRect(0, 0, 137, 270))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.page_1.setFont(font)
        self.page_1.setObjectName("page_1")
        self.toolBox.addItem(self.page_1, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 137, 270))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.page_2.setFont(font)
        self.page_2.setObjectName("page_2")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icones/icones/bureautique/white/info-256x256-460457.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.page_2, icon, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setStyleSheet("border-color: rgb(85, 85, 255);\n"
"selection-color: rgb(85, 85, 255);\n"
"border-radius:10px 0px;")
        self.page_3.setObjectName("page_3")
        self.toolBox.addItem(self.page_3, "")
        self.verticalLayout_2.addWidget(self.toolBox)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addWidget(self.widget)
        self.dockWidget.setWidget(self.dockWidgetContents)
        Interface.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.actionNouveau = QtWidgets.QAction(Interface)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icones/icones/bureautique/white/document-256x256-433820.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNouveau.setIcon(icon1)
        self.actionNouveau.setObjectName("actionNouveau")
        self.actioninterface_ui = QtWidgets.QAction(Interface)
        self.actioninterface_ui.setObjectName("actioninterface_ui")
        self.actionnew_ui = QtWidgets.QAction(Interface)
        self.actionnew_ui.setObjectName("actionnew_ui")
        self.actionOuvrir = QtWidgets.QAction(Interface)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icones/icones/bureautique/white/folder-256x256-460432.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOuvrir.setIcon(icon2)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionSauver = QtWidgets.QAction(Interface)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icones/icones/bureautique/white/floppy-256x256-460425.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSauver.setIcon(icon3)
        self.actionSauver.setObjectName("actionSauver")
        self.actionSauver_sous = QtWidgets.QAction(Interface)
        self.actionSauver_sous.setObjectName("actionSauver_sous")
        self.actionaction_new = QtWidgets.QAction(Interface)
        self.actionaction_new.setIcon(icon1)
        self.actionaction_new.setObjectName("actionaction_new")
        self.actionaction_open = QtWidgets.QAction(Interface)
        self.actionaction_open.setIcon(icon2)
        self.actionaction_open.setObjectName("actionaction_open")
        self.actionaction_save = QtWidgets.QAction(Interface)
        self.actionaction_save.setIcon(icon3)
        self.actionaction_save.setObjectName("actionaction_save")
        self.menuR_cents.addAction(self.actioninterface_ui)
        self.menuR_cents.addAction(self.actionnew_ui)
        self.menuFichier.addAction(self.actionNouveau)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.menuR_cents.menuAction())
        self.menuFichier.addAction(self.actionOuvrir)
        self.menuFichier.addAction(self.actionSauver)
        self.menuFichier.addAction(self.actionSauver_sous)
        self.menuBar.addAction(self.menuFichier.menuAction())
        self.menuBar.addAction(self.menuEdition.menuAction())
        self.menuBar.addAction(self.menuForm.menuAction())
        self.menuBar.addAction(self.menuVue.menuAction())
        self.menuBar.addAction(self.menuConfig.menuAction())
        self.menuBar.addAction(self.menuFen_tre.menuAction())
        self.menuBar.addAction(self.menuAide.menuAction())
        self.toolBar.addAction(self.actionaction_new)
        self.toolBar.addAction(self.actionaction_open)
        self.toolBar.addAction(self.actionaction_save)

        self.retranslateUi(Interface)
        self.toolBox.setCurrentIndex(1)
        self.toolBox.layout().setSpacing(8)
        QtCore.QMetaObject.connectSlotsByName(Interface)

    def retranslateUi(self, Interface):
        _translate = QtCore.QCoreApplication.translate
        Interface.setWindowTitle(_translate("Interface", "Interface"))
        self.menuFichier.setTitle(_translate("Interface", "Fichier"))
        self.menuR_cents.setTitle(_translate("Interface", "Récents"))
        self.menuEdition.setTitle(_translate("Interface", "Edition"))
        self.menuForm.setTitle(_translate("Interface", "Form"))
        self.menuVue.setTitle(_translate("Interface", "Vue"))
        self.menuConfig.setTitle(_translate("Interface", "Config"))
        self.menuFen_tre.setTitle(_translate("Interface", "Fenêtre"))
        self.menuAide.setTitle(_translate("Interface", "Aide"))
        self.toolBar.setWindowTitle(_translate("Interface", "toolBar"))
        self.dockWidget.setWindowTitle(_translate("Interface", "Widget"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_1), _translate("Interface", "Page 1"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("Interface", "Page2"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("Interface", "Page3"))
        self.actionNouveau.setText(_translate("Interface", "Nouveau"))
        self.actioninterface_ui.setText(_translate("Interface", "interface.ui"))
        self.actionnew_ui.setText(_translate("Interface", "new.ui"))
        self.actionOuvrir.setText(_translate("Interface", "Ouvrir"))
        self.actionSauver.setText(_translate("Interface", "Sauver"))
        self.actionSauver_sous.setText(_translate("Interface", "Sauver sous ..."))
        self.actionaction_new.setText(_translate("Interface", "action_new"))
        self.actionaction_new.setToolTip(_translate("Interface", "Nouveau"))
        self.actionaction_open.setText(_translate("Interface", "action_open"))
        self.actionaction_open.setToolTip(_translate("Interface", "Ouvrir"))
        self.actionaction_save.setText(_translate("Interface", "action_save"))
        self.actionaction_save.setToolTip(_translate("Interface", "Sauver"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Interface = QtWidgets.QMainWindow()
    ui = Ui_Interface()
    ui.setupUi(Interface)
    Interface.show()
    sys.exit(app.exec_())