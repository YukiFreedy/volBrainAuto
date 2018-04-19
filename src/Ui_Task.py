# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/task.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Task(object):
    def setupUi(self, Task):
        Task.setObjectName("Task")
        Task.resize(681, 56)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Task.sizePolicy().hasHeightForWidth())
        Task.setSizePolicy(sizePolicy)
        Task.setMinimumSize(QtCore.QSize(0, 56))
        Task.setMaximumSize(QtCore.QSize(16777215, 56))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Task)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filename = QtWidgets.QLabel(Task)
        self.filename.setObjectName("filename")
        self.horizontalLayout.addWidget(self.filename)
        self.date = QtWidgets.QLabel(Task)
        self.date.setObjectName("date")
        self.horizontalLayout.addWidget(self.date)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(15, -1, 15, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.processingLabel = QtWidgets.QLabel(Task)
        self.processingLabel.setObjectName("processingLabel")
        self.verticalLayout.addWidget(self.processingLabel)
        self.readyLabel = QtWidgets.QLabel(Task)
        self.readyLabel.setEnabled(True)
        self.readyLabel.setObjectName("readyLabel")
        self.verticalLayout.addWidget(self.readyLabel)
        self.errorLabel = QtWidgets.QLabel(Task)
        self.errorLabel.setObjectName("errorLabel")
        self.verticalLayout.addWidget(self.errorLabel)
        self.readyToLaunchLabel = QtWidgets.QLabel(Task)
        self.readyToLaunchLabel.setObjectName("readyToLaunchLabel")
        self.verticalLayout.addWidget(self.readyToLaunchLabel)
        self.deletedLabel = QtWidgets.QLabel(Task)
        self.deletedLabel.setObjectName("deletedLabel")
        self.verticalLayout.addWidget(self.deletedLabel)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.downloadButton = QtWidgets.QPushButton(Task)
        self.downloadButton.setObjectName("downloadButton")
        self.horizontalLayout.addWidget(self.downloadButton)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(Task)
        QtCore.QMetaObject.connectSlotsByName(Task)

    def retranslateUi(self, Task):
        _translate = QtCore.QCoreApplication.translate
        Task.setWindowTitle(_translate("Task", "Form"))
        self.filename.setText(_translate("Task", "filename"))
        self.date.setText(_translate("Task", "00/00/0000"))
        self.processingLabel.setToolTip(_translate("Task", "El trabajo se está procesando y podrá ser descargado en breves."))
        self.processingLabel.setText(_translate("Task", "Procesando..."))
        self.readyLabel.setToolTip(_translate("Task", "El trabajo se ha procesado y puede ser descargado."))
        self.readyLabel.setText(_translate("Task", "Procesado"))
        self.errorLabel.setText(_translate("Task", "Error"))
        self.readyToLaunchLabel.setToolTip(_translate("Task", "El trabajo será procesado."))
        self.readyToLaunchLabel.setText(_translate("Task", "En la cola"))
        self.deletedLabel.setToolTip(_translate("Task", "El fichero ha sido eliminado del servidor."))
        self.deletedLabel.setText(_translate("Task", "Eliminado"))
        self.downloadButton.setText(_translate("Task", "Descargar"))

