from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from Ui_MainWindow import Ui_MainWindow

### VENTANA PRINCIPAL ###
class volBrainClient(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super(volBrainClient, self).__init__(parent)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = volBrainClient()
    form.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
