from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_ProcessWindow import Ui_ProcessWindow
import threading

from TaskWidget import TaskWidget
import check_progress as check

# Esta clase auxiliar sirve para gestionar la descarga de archivos
# en un hilo a parte para evitar que se congele la interfaz.
class JobDownloadManager:
    def __init__(self):
        self.pendant = []
        self.running = False
    
    def startThread(self):
        if self.running: return
        
        self.running = True
        self.thread = threading.Thread(target = self.work)
        self.thread.start()
        
    def work(self):
        print('Thread started')
        while self.pendant:
            job = self.pendant.pop(0)
            print('Downloading: ' + job.filename)
            check.download_job_files(job)
            print('Downloaded: ' + job.filename)
        self.running = False
        print('Thread finished')
        
    def addJob(self, job):
        if job in self.pendant: return
        
        print('AddJob...')
        self.pendant += [job]
        
        if not self.running:
            self.startThread()
        
        
        
## VENTANA DE FILE PROGRESS ##
class ProcessWindow(QtWidgets.QMainWindow):

    def __init__(self, base_url, session, parent=None):
        super(ProcessWindow, self).__init__(parent)
        
        self.jobDownloadManager = JobDownloadManager()
        
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
        self.jobDownloadManager.addJob(job)
        self.sender().downloading()
        
