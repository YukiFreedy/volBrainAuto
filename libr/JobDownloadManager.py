from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import threading
import volbrainlib as volbrain

# Esta clase auxiliar sirve para gestionar la descarga de archivos
# en un hilo a parte para evitar que se congele la interfaz.
class JobDownloadManager(QtCore.QObject):
    # El manager enviará una señal cuando la descarga de un trabajo
    # haya terminado. Mandará como parámetro el trabajo.
    downloaded = pyqtSignal(volbrain.Job)
    
    def __init__(self, folder = None, createSubfolder = True, downloadMni = True, downloadNat = True, downloadPdf = True):
        super(JobDownloadManager, self).__init__()
        self.pendant = []
        self.running = False
        self.setConfig(folder, createSubfolder, downloadMni, downloadNat, downloadPdf)
    
    def setConfig(self, folder, createSubfolder, downloadMni, downloadNat, downloadPdf):
        self.folder = folder
        self.createSubfolder = createSubfolder
        
        self.downloadMni = downloadMni
        self.downloadNat = downloadNat
        self.downloadPdf = downloadPdf
    
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
            volbrain.download_job_files(job, self.folder, self.createSubfolder, self.downloadMni, self.downloadNat, self.downloadPdf)
            print('Downloaded: ' + job.filename)
            self.downloaded.emit(job)
        self.running = False
        print('Thread finished')
        
    def addJob(self, job):
        if job in self.pendant: return
        
        self.pendant += [job]
        
        if not self.running:
            self.startThread()
            
    def isDownloading(self):
        return self.running
        

