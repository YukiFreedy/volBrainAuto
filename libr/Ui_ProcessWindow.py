# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/processwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProcessWindow(object):
    def setupUi(self, ProcessWindow):
        ProcessWindow.setObjectName("ProcessWindow")
        ProcessWindow.resize(781, 488)
        self.centralwidget = QtWidgets.QWidget(ProcessWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.jobList = QtWidgets.QWidget()
        self.jobList.setGeometry(QtCore.QRect(0, 0, 761, 395))
        self.jobList.setObjectName("jobList")
        self.jobListLayout = QtWidgets.QVBoxLayout(self.jobList)
        self.jobListLayout.setContentsMargins(0, 0, 0, 0)
        self.jobListLayout.setObjectName("jobListLayout")
        self.scrollArea.setWidget(self.jobList)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.previousButton = QtWidgets.QPushButton(self.centralwidget)
        self.previousButton.setObjectName("previousButton")
        self.horizontalLayout_2.addWidget(self.previousButton)
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout_2.addWidget(self.nextButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.downloadPageButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadPageButton.setObjectName("downloadPageButton")
        self.horizontalLayout_2.addWidget(self.downloadPageButton)
        self.downloadConfigButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadConfigButton.setObjectName("downloadConfigButton")
        self.horizontalLayout_2.addWidget(self.downloadConfigButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        ProcessWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ProcessWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 781, 20))
        self.menubar.setObjectName("menubar")
        ProcessWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ProcessWindow)
        self.statusbar.setObjectName("statusbar")
        ProcessWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ProcessWindow)
        QtCore.QMetaObject.connectSlotsByName(ProcessWindow)

    def retranslateUi(self, ProcessWindow):
        _translate = QtCore.QCoreApplication.translate
        ProcessWindow.setWindowTitle(_translate("ProcessWindow", "Cola de trabajos"))
        self.previousButton.setText(_translate("ProcessWindow", "<"))
        self.nextButton.setText(_translate("ProcessWindow", ">"))
        self.downloadPageButton.setText(_translate("ProcessWindow", "Descargar página completa"))
        self.downloadConfigButton.setText(_translate("ProcessWindow", "Configurar descarga"))

