from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import threading
import volbrainlib as volbrain

# Esta clase sirve para gestionar la carga de archivos
# en un hilo a parte para evitar que se congele la interfaz.
class JobUploadManager(QtCore.QObject):

    uploaded = pyqtSignal(int, int)
    
    def __init__(self, base_url, session):
        super(JobUploadManager, self).__init__()
        self.running = False
        self.base_url = base_url
        self.session = session
        self.pendant = []
    

    def startThread(self):
        if self.running: return
        
        self.running = True
        self.thread = threading.Thread(target = self.work)
        self.thread.start()
        
    def work(self):
        print('Upload thread started')
        while self.pendant:
            files = self.pendant.pop(0)
            print('Loading')
            uploaded = volbrain.upload_job(self.base_url, self.session, files)
            print('Loaded')
            print(uploaded, len(files))
            self.uploaded.emit(uploaded, len(files))
        self.running = False
        print('Thread finished')
    
    # Añade una lista de FileUpload para ser subidos.
    def addJobs(self, jobs):
        self.pendant += [jobs]
        
        if not self.running:
            self.startThread()
            
    def isLoading(self):
        return self.running
        

