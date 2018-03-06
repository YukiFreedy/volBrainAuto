# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/login.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(400, 228)
        self.verticalLayout = QtWidgets.QVBoxLayout(Login)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(Login)
        self.label_3.setStyleSheet("font-size: 16pt;")
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.loginErrorLabel = QtWidgets.QLabel(Login)
        self.loginErrorLabel.setEnabled(False)
        self.loginErrorLabel.setStyleSheet("color: red;")
        self.loginErrorLabel.setObjectName("loginErrorLabel")
        self.verticalLayout.addWidget(self.loginErrorLabel)
        self.label = QtWidgets.QLabel(Login)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.email = QtWidgets.QLineEdit(Login)
        self.email.setObjectName("email")
        self.verticalLayout.addWidget(self.email)
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.password = QtWidgets.QLineEdit(Login)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.verticalLayout.addWidget(self.password)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Login)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Login)
        self.buttonBox.accepted.connect(Login.accept)
        self.buttonBox.rejected.connect(Login.reject)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "volBrain Client - Login"))
        self.label_3.setText(_translate("Login", "Iniciar sesión"))
        self.loginErrorLabel.setText(_translate("Login", "Error al iniciar sesión."))
        self.label.setText(_translate("Login", "Correo electrónico"))
        self.label_2.setText(_translate("Login", "Contraseña"))

