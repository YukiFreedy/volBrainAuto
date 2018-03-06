from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from Ui_MainWindow import Ui_MainWindow
from Ui_Login import Ui_Login
from Ui_ProcessWindow import Ui_ProcessWindow
from TaskWidget import TaskWidget

import check_progress as check


def getFiles():
    return []

currentFiles = []

### VENTANA PRINCIPAL ###
class volBrainClient(QtWidgets.QMainWindow):

    def __init__(self, base_url, session, parent=None):
        super(volBrainClient, self).__init__(parent)
        
        self.session = session
        self.base_url = base_url
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.selectFilesButton.clicked.connect(self.chooseFile)
        self.ui.cleanButton.clicked.connect(self.cleanList)
        self.ui.showJobsButton.clicked.connect(self.openProcessWindow)
        
    def chooseFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            currentFiles.append(fileName)
            self.ui.listWidget.addItem(fileName)

    def cleanList(self):
        currentFiles = []
        self.ui.listWidget.clear()

    def openProcessWindow(self):
        self.win = ProcessWindow(self.base_url, self.session)
        self.win.show()

## VENTANA DE FILE PROGRESS ##
class ProcessWindow(QtWidgets.QMainWindow):

    def __init__(self, base_url, session, parent=None):
        super(ProcessWindow, self).__init__(parent)
        
        self.ui = Ui_ProcessWindow()
        self.ui.setupUi(self)

        self.ui.backButton.clicked.connect(self.close)
        
        (jobs, hasNext) = check.get_jobs_in_page(base_url, session)
        
        for job in jobs:      
            taskWidget = TaskWidget(job)
            taskWidget.download.connect(self.downloadJob)
            self.ui.jobListLayout.addWidget(taskWidget)
        
        self.ui.jobListLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
    
    #SLOT. El usuario ha solicitado la descarga de un fichero.
    def downloadJob(self, job):
        print(job.filename)
        check.download_job_files(job, None, True)

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
        form = volBrainClient(base_url, session)
        form.show()
        res = app.exec_()

if __name__ == "__main__":
    main()
