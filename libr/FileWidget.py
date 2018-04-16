from PyQt5 import QtWidgets
from Ui_File import Ui_File
from PyQt5.QtGui import QIntValidator


class FileWidget(QtWidgets.QWidget):
    
    def __init__(self, file, parent=None):
        super(FileWidget, self).__init__(parent)

        self.ui = Ui_File()
        self.ui.setupUi(self)
        
        self.ui.filename.setText(file)

        self.file = file

        self.ui.lineEdit.setValidator(QIntValidator(0, 150, self) )

        self.ui.checkUpload.setChecked(True)
        
        self.ui.volCheck.setChecked(True)
        self.ui.volCheck.clicked.connect(self.uncheckCeres)
        self.ui.ceresCheck.clicked.connect(self.uncheckVol)

    def uncheckCeres(self):
        self.ui.ceresCheck.setChecked(False)
        self.ui.volCheck.setChecked(True)

    def uncheckVol(self):
        self.ui.volCheck.setChecked(False)
        self.ui.ceresCheck.setChecked(True)

    def getGenre(self):
        if(self.ui.radioMan.isChecked):
            return "Male"
        else:
            return "Female"

    def getFile(self):
        return self.file

    def getChecked(self):
        return self.ui.checkUpload.isChecked

    def getAge(self):
        return self.ui.lineEdit.text

    def getPipeline(self):
        if self.ui.volCheck.isChecked():
            return 1
        else:
            return 3
