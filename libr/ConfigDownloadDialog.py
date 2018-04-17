from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from Ui_ConfigDownloadDialog import Ui_ConfigDownloadDialog

import configparser
import os

## DIALOGO DE CONFIGURACION DE LA DESCARGA ##        
class ConfigDownloadDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(ConfigDownloadDialog, self).__init__(parent)
        
        self.ui = Ui_ConfigDownloadDialog()
        self.ui.setupUi(self)
        
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        
        self.ui.targetFolderLabel.setText(self.config.get('download', 'folder', fallback = os.getcwd()))
        self.ui.targetFolderBtn.clicked.connect(self.openFolderDialog)
        
        self.ui.createSubfolderCheckbox.setChecked(self.config.getboolean('download', 'create_subfolder', fallback=True))
        
        self.ui.downloadMniCheckbox.setChecked(self.config.getboolean('download', 'download_mni', fallback = True))
        self.ui.downloadNatCheckbox.setChecked(self.config.getboolean('download', 'download_nat', fallback = True))
        self.ui.downloadPdfCheckbox.setChecked(self.config.getboolean('download', 'download_pdf', fallback = True))
        
        self.ui.buttonBox.accepted.connect(self.save)
    
    def openFolderDialog(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Selecciona una carpeta de destino"))
        if (folder is not ''):
            self.ui.targetFolderLabel.setText(os.path.join(folder, ''))
    
    def save(self):
        self.config['download'] = {}
        self.config['download']['folder'] = self.ui.targetFolderLabel.text()
        self.config['download']['create_subfolder'] = str(self.ui.createSubfolderCheckbox.isChecked())
        
        self.config['download']['download_mni'] = str(self.ui.downloadMniCheckbox.isChecked())
        self.config['download']['download_nat'] = str(self.ui.downloadNatCheckbox.isChecked())
        self.config['download']['download_pdf'] = str(self.ui.downloadPdfCheckbox.isChecked())
        
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
    

