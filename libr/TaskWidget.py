from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from Ui_Task import Ui_Task

import check_progress as check

class TaskWidget(QtWidgets.QWidget):
    
    view = pyqtSignal(check.Job)
    download = pyqtSignal(check.Job)
    
    def __init__(self, job, parent=None):
        super(TaskWidget, self).__init__(parent)

        self.ui = Ui_Task()
        self.ui.setupUi(self)
        
        self.ui.filename.setText(job.filename)
        self.ui.date.setText(job.date)
        
        self.job = job
        
        if job.state == 'ready_to_launch':
            self.ui.readyLabel.hide()
            self.ui.processingLabel.hide()
        elif job.state == 'ready':
            self.ui.processingLabel.hide()
            self.ui.readyToLaunchLabel.hide();
        elif job.state == 'launched':
            self.ui.readyToLaunchLabel.hide()
            self.ui.readyLabel.hide()
            
        self.ui.downloadButton.clicked.connect(self.requestDownload)
    
    # Envía una señal para notificar que se ha hecho clic
    # en el botón de descargar.
    def requestDownload(self):
        self.download.emit(self.job)
        pass
    
    # Sirve para notificar al TaskWidget que el trabajo que representa
    # está siendo descargado.
    def downloading(self):
        self.ui.downloadButton.setText("Descargando...")
        self.ui.downloadButton.setEnabled(False)
