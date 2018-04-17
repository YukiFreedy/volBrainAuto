# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/file.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_File(object):
    def setupUi(self, File):
        File.setObjectName("File")
        File.resize(681, 56)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(File.sizePolicy().hasHeightForWidth())
        File.setSizePolicy(sizePolicy)
        File.setMinimumSize(QtCore.QSize(0, 56))
        File.setMaximumSize(QtCore.QSize(16777215, 56))
        self.horizontalLayout = QtWidgets.QHBoxLayout(File)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filename = QtWidgets.QLabel(File)
        self.filename.setObjectName("filename")
        self.horizontalLayout.addWidget(self.filename)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ceresCheck = QtWidgets.QCheckBox(File)
        self.ceresCheck.setObjectName("ceresCheck")
        self.verticalLayout_3.addWidget(self.ceresCheck)
        self.volCheck = QtWidgets.QCheckBox(File)
        self.volCheck.setObjectName("volCheck")
        self.verticalLayout_3.addWidget(self.volCheck)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(File)
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setMaxLength(3)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(15, -1, 15, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioMan = QtWidgets.QRadioButton(File)
        self.radioMan.setChecked(True)
        self.radioMan.setObjectName("radioMan")
        self.verticalLayout.addWidget(self.radioMan)
        self.radioWoman = QtWidgets.QRadioButton(File)
        self.radioWoman.setObjectName("radioWoman")
        self.verticalLayout.addWidget(self.radioWoman)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.checkUpload = QtWidgets.QCheckBox(File)
        self.checkUpload.setObjectName("checkUpload")
        self.horizontalLayout.addWidget(self.checkUpload)
        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(File)
        QtCore.QMetaObject.connectSlotsByName(File)

    def retranslateUi(self, File):
        _translate = QtCore.QCoreApplication.translate
        File.setWindowTitle(_translate("File", "Form"))
        self.filename.setText(_translate("File", "filename"))
        self.ceresCheck.setText(_translate("File", "Ceres"))
        self.volCheck.setText(_translate("File", "volBrain"))
        self.lineEdit.setPlaceholderText(_translate("File", "Edad"))
        self.radioMan.setText(_translate("File", "Hombre"))
        self.radioWoman.setText(_translate("File", "M&ujer"))
        self.checkUpload.setText(_translate("File", "Subir"))

