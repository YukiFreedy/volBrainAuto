from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from Ui_MainWindow import Ui_MainWindow
from Ui_Login import Ui_Login

import check_progress as check

### VENTANA PRINCIPAL ###
class volBrainClient(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super(volBrainClient, self).__init__(parent)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
## VENTANA DE LOGIN ##
class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.loginErrorLabel.setVisible(False)
    
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
        app.exec_()
    
if __name__ == "__main__":
    main()
