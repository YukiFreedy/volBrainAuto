from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from Ui_Task import Ui_Task

import volbrainlib as volbrain

class TaskWidget(QtWidgets.QWidget):
    
    view = pyqtSignal(volbrain.Job)
    download = pyqtSignal(volbrain.Job)
    
    def __init__(self, job, parent=None):
        super(TaskWidget, self).__init__(parent)

        self.ui = Ui_Task()
        self.ui.setupUi(self)
        
        self.ui.filename.setText(job.filename)
        self.ui.date.setText(job.date)
        
        self.job = job
        
        self.hideLabels()
        
        if job.state == 'ready_to_launch':
            self.ui.readyToLaunchLabel.show();
        elif job.state == 'ready':
            self.ui.downloadButton.setEnabled(True)
            self.ui.readyLabel.show()
        elif job.state == 'launched':
            self.ui.processingLabel.show();
        elif job.state == 'deleted':
            self.ui.deletedLabel.show();
            
        self.ui.downloadButton.clicked.connect(self.requestDownload)
    
    def hideLabels(self):    
        self.ui.downloadButton.setEnabled(False)
        self.ui.readyLabel.hide()
        self.ui.processingLabel.hide()
        self.ui.readyToLaunchLabel.hide();
        self.ui.deletedLabel.hide();
    
    def getJob(self):
        return self.job
    
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
        
    # Este método sirve para notificar al TaskWidget que el trabajo
    # que representa ha sido descargado.
    def downloaded(self):
        self.ui.downloadButton.setText("Descargado")
        self.ui.downloadButton.setEnabled(False)
