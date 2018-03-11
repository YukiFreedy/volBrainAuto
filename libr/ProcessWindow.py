from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialogButtonBox, QDialog
from Ui_ProcessWindow import Ui_ProcessWindow
from Ui_ConfigDownloadDialog import Ui_ConfigDownloadDialog
import threading

from TaskWidget import TaskWidget
import check_progress as check
import configparser

# Esta clase auxiliar sirve para gestionar la descarga de archivos
# en un hilo a parte para evitar que se congele la interfaz.
class JobDownloadManager(QtCore.QObject):
    # El manager enviará una señal cuando la descarga de un trabajo
    # haya terminado. Mandará como parámetro el trabajo.
    downloaded = pyqtSignal(check.Job)
    
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
            check.download_job_files(job, self.folder, self.createSubfolder, self.downloadMni, self.downloadNat, self.downloadPdf)
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
            
    def isDownloading(self):
        return self.running
        

## DIALOGO DE CONFIGURACION DE LA DESCARGA ##        
class ConfigDownloadDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(ConfigDownloadDialog, self).__init__(parent)
        
        self.ui = Ui_ConfigDownloadDialog()
        self.ui.setupUi(self)
        
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        
        self.ui.targetFolderLabel.setText(self.config.get('download', 'folder', fallback = './'))
        self.ui.createSubfolderCheckbox.setChecked(self.config.getboolean('download', 'create_subfolder', fallback=True))
        
        self.ui.downloadMniCheckbox.setChecked(self.config.getboolean('download', 'download_mni', fallback = True))
        self.ui.downloadNatCheckbox.setChecked(self.config.getboolean('download', 'download_nat', fallback = True))
        self.ui.downloadPdfCheckbox.setChecked(self.config.getboolean('download', 'download_pdf', fallback = True))
        
        self.ui.buttonBox.accepted.connect(self.save)
    
    def save(self):
        self.config['download'] = {}
        self.config['download']['folder'] = self.ui.targetFolderLabel.text()
        self.config['download']['create_subfolder'] = str(self.ui.createSubfolderCheckbox.isChecked())
        
        self.config['download']['download_mni'] = str(self.ui.downloadMniCheckbox.isChecked())
        self.config['download']['download_nat'] = str(self.ui.downloadNatCheckbox.isChecked())
        self.config['download']['download_pdf'] = str(self.ui.downloadPdfCheckbox.isChecked())
        
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
    


## VENTANA DE FILE PROGRESS ##
class ProcessWindow(QtWidgets.QMainWindow):

    def __init__(self, base_url, session, parent=None):
        super(ProcessWindow, self).__init__(parent)
        
        
        self.baseUrl = base_url
        self.session = session
        
        self.taskWidgets = []
        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        # Se crear el JobDownloadManager que se encargará de mantener
        # una cola de descargas en un hilo independiente.
        self.jobDownloadManager = JobDownloadManager()
        self.jobDownloadManager.downloaded.connect(self.jobDownloaded)
        
        self.loadConfig()
        
        # Configurar la interfaz #
        self.ui = Ui_ProcessWindow()
        self.ui.setupUi(self)
        
        
        # Cargar los trabajos #
        self.currentPage = 1
        self.pages = check.count_pages(self.baseUrl, self.session)
        self.updateNavButtons()
        self.loadJobs()
        
        # Configurar SLOTS
        self.ui.downloadConfigButton.clicked.connect(self.openConfigDownloadDialog)
        self.ui.nextButton.clicked.connect(self.nextPage)
        self.ui.previousButton.clicked.connect(self.previousPage)
        
    
    # SLOT. Este slot se ejecuta cuando el usuario solicita la descarga
    # de algún trabajo.
    def downloadJob(self, job):
        # El JobDownloadManager se encarga de gestionar la descarga
        # en un hilo a parte.
        self.jobDownloadManager.addJob(job)
        
        # Notificamos al widget que la descarga ha comenzado.
        self.sender().downloading()
    
    # SLOT. Este slot se ejecuta cuando una de las tareas se ha descargado.
    def jobDownloaded(self, job):
        for taskWidget in self.taskWidgets:
            if (taskWidget.getJob() == job):
                taskWidget.downloaded()
                break
    
    # SLOT.
    def openConfigDownloadDialog(self):
        dialog = ConfigDownloadDialog(self)
        
        if (dialog.exec_() == QDialog.Accepted):
            # Actualizar la configuración.
            self.loadConfig()
    
    # SLOT.
    def nextPage(self):
        self.currentPage += 1
        self.updateNavButtons()
        self.loadJobs()
    
    # SLOT.
    def previousPage(self):
        self.currentPage -= 1
        self.updateNavButtons()
        self.loadJobs()
    
    def updateNavButtons(self):
        if self.currentPage == 1: self.ui.previousButton.setEnabled(False)
        else: self.ui.previousButton.setEnabled(True)

        if self.currentPage == self.pages: self.ui.nextButton.setEnabled(False)
        else: self.ui.nextButton.setEnabled(True)
        
        self.setWindowTitle("Cola de trabajos (" + str(self.currentPage) + '/' + str(self.pages) + ')')
    
    # Cargar lista de trabajos.
    def loadJobs(self):
        # Cargar la lista de trabajos de la página actual.
        (jobs, hasNext) = check.get_jobs_in_page(self.baseUrl, self.session, self.currentPage)
        
        
        self.ui.jobListLayout.removeItem(self.spacerItem)
        
        # taskWidgets mantiene una lista de los widgets que representan las tareas
        # y que están siendo mostrados.
        # Eliminar widgets anteriores.
        for j in self.taskWidgets: j.setParent(None)
        self.taskWidgets = []
        
        # Se añaden los trabajos a la interfaz.
        for job in jobs: 
            taskWidget = TaskWidget(job)
            taskWidget.download.connect(self.downloadJob)
            self.ui.jobListLayout.addWidget(taskWidget)
            
            self.taskWidgets += [taskWidget]
        

        self.ui.jobListLayout.addItem(self.spacerItem)
    
    def loadConfig(self):
        # Cargar la configuración para saber dónde descargar los archivos #
        config = configparser.ConfigParser()
        config.read('config.ini')
        folder = config.get('download', 'folder', fallback = './')
        createSubfolder = config.getboolean('download', 'create_subfolder', fallback=True)
        
        # Configuración para saber qué ficheros descargar.
        downloadMni = config.getboolean('download', 'download_mni', fallback = True)
        downloadNat = config.getboolean('download', 'download_nat', fallback = True)
        downloadPdf = config.getboolean('download', 'download_pdf', fallback = True)
        
        
        self.jobDownloadManager.setConfig(folder, createSubfolder, downloadMni, downloadNat, downloadPdf)
        
    def closeEvent(self, event):
        if self.jobDownloadManager.isDownloading():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Se está descargando un fichero. Si cierras la aplicación no terminará la descarga.")
            msg.setInformativeText("¿Seguro que quieres cerrar esta ventana?")
            msg.setWindowTitle("¿Quieres cerrar la ventana?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg.exec_() == QMessageBox.No: event.ignore()
            else: event.accept()
        else:
            event.accept()
        
