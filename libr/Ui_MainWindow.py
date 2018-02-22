# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(635, 324)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.selectFilesButton = QtWidgets.QPushButton(self.centralWidget)
        self.selectFilesButton.setObjectName("selectFilesButton")
        self.horizontalLayout.addWidget(self.selectFilesButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.uploadFilesButton = QtWidgets.QPushButton(self.centralWidget)
        self.uploadFilesButton.setObjectName("uploadFilesButton")
        self.horizontalLayout_3.addWidget(self.uploadFilesButton)
        self.cleanButton = QtWidgets.QPushButton(self.centralWidget)
        self.cleanButton.setObjectName("cleanButton")
        self.horizontalLayout_3.addWidget(self.cleanButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.loadingBar = QtWidgets.QProgressBar(self.centralWidget)
        self.loadingBar.setProperty("value", 24)
        self.loadingBar.setObjectName("loadingBar")
        self.horizontalLayout_2.addWidget(self.loadingBar)
        self.showJobsButton = QtWidgets.QPushButton(self.centralWidget)
        self.showJobsButton.setObjectName("showJobsButton")
        self.horizontalLayout_2.addWidget(self.showJobsButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 635, 25))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "volBrain Client"))
        self.selectFilesButton.setText(_translate("MainWindow", "Explorar ficheros"))
        self.uploadFilesButton.setText(_translate("MainWindow", "Subir ficheros"))
        self.cleanButton.setText(_translate("MainWindow", "Limpiar lista"))
        self.showJobsButton.setText(_translate("MainWindow", "Ver trabajos"))

