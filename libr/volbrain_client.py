from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys

from Ui_MainWindow import Ui_MainWindow
from Ui_Login import Ui_Login
from Ui_ProcessWindow import Ui_ProcessWindow

import check_progress as check


def getFiles():
    return []

currentFiles = []

### VENTANA PRINCIPAL ###
class volBrainClient(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(volBrainClient, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        def chooseFile():
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                currentFiles.append(fileName)
                self.ui.listWidget.addItem(fileName)

        def cleanList():
            currentFiles = []
            self.ui.listWidget.clear()

        def openProcessWindow():
            win = ProcessWindow()
            win.show()

        self.ui.selectFilesButton.clicked.connect(chooseFile)
        self.ui.cleanButton.clicked.connect(cleanList)
        self.ui.showJobsButton.clicked.connect(openProcessWindow)

## VENTANA DE FILE PROGRESS ##
class ProcessWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(ProcessWindow, self).__init__(parent)

        self.ui = Ui_ProcessWindow()
        self.ui.setupUi(self)

        def close():
            self.close()

        self.ui.pushButton.clicked.connect(close)

## VENTANA DE LOGIN ##
class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.loginErrorLabel.setVisible(False)
        self.ui.email.setText("vicrivaz@inf.upv.es")
        self.ui.password.setText("09081996")

    def getLogin(self):
        return (self.ui.email.text(), self.ui.password.text())

    def showError(self, show):
        self.ui.loginErrorLabel.setVisible(show)

def main():
    app = QtWidgets.QApplication(sys.argv)

    base_url = 'http://volbrain.upv.es/'

    login = LoginDialog()
    login.showError(False)

    loginOk = False
    rejected = False

    while not loginOk:
        res = login.exec()
        if res == QtWidgets.QDialog.Rejected:
            rejected = True
            break

        (email, password) = login.getLogin()

        try:
            session = check.login(base_url, email, password)
            loginOk = True
            login.showError(False)
        except check.LoginException:
            login.showError(True)

    if not rejected:
        form = volBrainClient()
        form.show()
        res = app.exec_()

if __name__ == "__main__":
    main()
