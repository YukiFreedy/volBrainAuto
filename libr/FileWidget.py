from PyQt5 import QtWidgets
from Ui_File import Ui_File


class FileWidget(QtWidgets.QWidget):
    
    def __init__(self, file, parent=None):
        super(FileWidget, self).__init__(parent)

        self.ui = Ui_File()
        self.ui.setupUi(self)
        
        self.ui.filename.setText(file)

        self.file = file

    def getGenre(self):
        if(self.ui.radioMan.isChecked):
            return "M"
        else:
            return "F"

    def getFile(self):
        return self.file

    def getChecked(self):
        return self.ui.checkUpload.isChecked

    def getAge(self):
        return 18
