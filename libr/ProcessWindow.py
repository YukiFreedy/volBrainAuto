from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from Ui_ProcessWindow import Ui_ProcessWindow
import threading

from TaskWidget import TaskWidget
import check_progress as check

# Esta clase auxiliar sirve para gestionar la descarga de archivos
# en un hilo a parte para evitar que se congele la interfaz.
class JobDownloadManager(QtCore.QObject):
    # El manager enviará una señal cuando la descarga de un trabajo
    # haya terminado. Mandará como parámetro el trabajo.
    downloaded = pyqtSignal(check.Job)
    
    def __init__(self):
        super(JobDownloadManager, self).__init__()
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
            self.downloaded.emit(job)
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
        self.jobDownloadManager.downloaded.connect(self.jobDownloaded)
        
        self.ui = Ui_ProcessWindow()
        self.ui.setupUi(self)

        self.ui.backButton.clicked.connect(self.close)
        
        (jobs, hasNext) = check.get_jobs_in_page(base_url, session)
        
        self.taskWidgets = []
        
        for job in jobs: 
            taskWidget = TaskWidget(job)
            taskWidget.download.connect(self.downloadJob)
            self.ui.jobListLayout.addWidget(taskWidget)
            
            self.taskWidgets += [taskWidget]
        
        self.ui.jobListLayout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
    
    #SLOT. Este slot se ejecuta cuando el usuario solicita la descarga
    # de algún trabajo.
    def downloadJob(self, job):
        # El JobDownloadManager se encarga de gestionar la descarga
        # en un hilo a parte.
        self.jobDownloadManager.addJob(job)
        
        # Notificamos al widget que la descarga ha comenzado.
        self.sender().downloading()
    
    def jobDownloaded(self, job):
        for taskWidget in self.taskWidgets:
            if (taskWidget.getJob() == job):
                taskWidget.downloaded()
                break
        
