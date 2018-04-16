from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys

from Ui_MainWindow import Ui_MainWindow
from Ui_Login import Ui_Login

import ProcessWindow
import volbrainlib as volbrain

from FileWidget import FileWidget

from volbrainlib import FileUpload

import threading


def getFiles():
    return []


### VENTANA PRINCIPAL ###
class volBrainClient(QtWidgets.QMainWindow):

    def __init__(self, base_url, session, email, password, parent=None):
        super(volBrainClient, self).__init__(parent)
        
        self.session = session
        self.base_url = base_url
        
        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.selectFilesButton.clicked.connect(self.chooseFile)
        self.ui.cleanButton.clicked.connect(self.cleanList)
        self.ui.showJobsButton.clicked.connect(self.openProcessWindow)
        self.ui.uploadFilesButton.clicked.connect(self.uploadSelected)

        self.email = email
        self.password = password
        
        self.fileWidgets = []

    def uploadSelected(self):
        files = []
        for w in self.fileWidgets:
            if(w.getChecked()):
                files += [FileUpload(w.getFile(), w.getGenre(), w.getAge(), w.getPipeline())]
        self.upload(files)

    def upload(self, files):
        self.running = True
        self.thread = threading.Thread(target = self.work(files))
        self.thread.start()
        
    def work(self, files):
        volbrain.upload_job(self.base_url, self.session, files)

    def chooseFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Selecciona un fichero", "","Zip Files (*.zip)", options=options)
        if fileName:
            self.ui.jobListLayout.removeItem(self.spacerItem)
            self.fileWidgets += [FileWidget(fileName)]
            for w in self.fileWidgets:
                w.setParent(None)
            for w in self.fileWidgets:
                self.ui.jobListLayout.addWidget(w)
            self.ui.jobListLayout.addItem(self.spacerItem)

    def cleanList(self):
        for w in self.fileWidgets:
            w.setParent(None)
        self.fileWidgets = []

    def openProcessWindow(self):
        self.win = ProcessWindow.ProcessWindow(self.base_url, self.session)
        self.win.show()


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
            session = volbrain.login(base_url, email, password)
            loginOk = True
            login.showError(False)
        except volbrain.LoginException:
            login.showError(True)

    if not rejected:
        form = volBrainClient(base_url, session, email, password)
        form.show()
        res = app.exec_()

if __name__ == "__main__":
    main()
