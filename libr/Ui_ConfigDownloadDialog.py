# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/configdownloaddialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConfigDownloadDialog(object):
    def setupUi(self, ConfigDownloadDialog):
        ConfigDownloadDialog.setObjectName("ConfigDownloadDialog")
        ConfigDownloadDialog.resize(527, 302)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConfigDownloadDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(ConfigDownloadDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(12, -1, 12, 14)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.targetFolderLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetFolderLabel.sizePolicy().hasHeightForWidth())
        self.targetFolderLabel.setSizePolicy(sizePolicy)
        self.targetFolderLabel.setStyleSheet("color: rgb(46, 52, 54);")
        self.targetFolderLabel.setObjectName("targetFolderLabel")
        self.horizontalLayout.addWidget(self.targetFolderLabel)
        self.targetFolderBtn = QtWidgets.QPushButton(self.groupBox)
        self.targetFolderBtn.setObjectName("targetFolderBtn")
        self.horizontalLayout.addWidget(self.targetFolderBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.createSubfolderCheckbox = QtWidgets.QCheckBox(self.groupBox)
        self.createSubfolderCheckbox.setObjectName("createSubfolderCheckbox")
        self.verticalLayout_2.addWidget(self.createSubfolderCheckbox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(ConfigDownloadDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.downloadMniCheckbox = QtWidgets.QCheckBox(self.groupBox_2)
        self.downloadMniCheckbox.setObjectName("downloadMniCheckbox")
        self.verticalLayout_3.addWidget(self.downloadMniCheckbox)
        self.downloadNatCheckbox = QtWidgets.QCheckBox(self.groupBox_2)
        self.downloadNatCheckbox.setObjectName("downloadNatCheckbox")
        self.verticalLayout_3.addWidget(self.downloadNatCheckbox)
        self.downloadPdfCheckbox = QtWidgets.QCheckBox(self.groupBox_2)
        self.downloadPdfCheckbox.setObjectName("downloadPdfCheckbox")
        self.verticalLayout_3.addWidget(self.downloadPdfCheckbox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConfigDownloadDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ConfigDownloadDialog)
        self.buttonBox.accepted.connect(ConfigDownloadDialog.accept)
        self.buttonBox.rejected.connect(ConfigDownloadDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigDownloadDialog)

    def retranslateUi(self, ConfigDownloadDialog):
        _translate = QtCore.QCoreApplication.translate
        ConfigDownloadDialog.setWindowTitle(_translate("ConfigDownloadDialog", "Configuración de la descarga"))
        self.groupBox.setTitle(_translate("ConfigDownloadDialog", "Destino"))
        self.label.setText(_translate("ConfigDownloadDialog", "Carpeta de destino:"))
        self.targetFolderLabel.setText(_translate("ConfigDownloadDialog", "github.com/rafaelgc"))
        self.targetFolderBtn.setText(_translate("ConfigDownloadDialog", "Cambiar carpeta"))
        self.createSubfolderCheckbox.setText(_translate("ConfigDownloadDialog", "Crear subcarpeta para cada trabajo."))
        self.groupBox_2.setTitle(_translate("ConfigDownloadDialog", "Ficheros"))
        self.downloadMniCheckbox.setText(_translate("ConfigDownloadDialog", "Descargar MNI"))
        self.downloadNatCheckbox.setText(_translate("ConfigDownloadDialog", "Descargar NAT"))
        self.downloadPdfCheckbox.setText(_translate("ConfigDownloadDialog", "Descargar PDF"))

