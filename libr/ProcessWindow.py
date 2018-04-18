from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QFileDialog
from Ui_ProcessWindow import Ui_ProcessWindow
import os

from TaskWidget import TaskWidget
import volbrainlib as volbrain
import configparser
import JobDownloadManager
import ConfigDownloadDialog

## VENTANA DE FILE PROGRESS ##
class ProcessWindow(QtWidgets.QMainWindow):

    def __init__(self, base_url, session, parent=None):
        super(ProcessWindow, self).__init__(parent)
        
        
        self.baseUrl = base_url
        self.session = session
        
        self.taskWidgets = []
        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        # Se crea el JobDownloadManager que se encargará de mantener
        # una cola de descargas en un hilo independiente.
        self.jobDownloadManager = JobDownloadManager.JobDownloadManager()
        self.jobDownloadManager.downloaded.connect(self.jobDownloaded)
        
        self.loadConfig()
        
        # Configurar la interfaz #
        self.ui = Ui_ProcessWindow()
        self.ui.setupUi(self)
        
        
        # Cargar los trabajos #
        self.currentPage = 1
        self.pages = volbrain.count_pages(self.baseUrl, self.session)
        self.updateNavButtons()
        self.loadJobs()
        
        # Timer para recargar la página automáticamente #
        self.reloadTimer = QTimer()
        self.reloadTimer.setInterval(4 * 60000)
        self.reloadTimer.timeout.connect(self.loadJobs)
        self.reloadTimer.start()
        
        # Configurar SLOTS
        self.ui.downloadConfigButton.clicked.connect(self.openConfigDownloadDialog)
        self.ui.nextButton.clicked.connect(self.nextPage)
        self.ui.previousButton.clicked.connect(self.previousPage)
        self.ui.downloadPageButton.clicked.connect(self.downloadPage)
        
    
    # SLOT. Este slot se ejecuta cuando el usuario solicita la descarga
    # de algún trabajo.
    def downloadJob(self, job):
        # El JobDownloadManager se encarga de gestionar la descarga
        # en un hilo a parte.
        self.jobDownloadManager.addJob(job)
        
        # Notificamos al widget que la descarga ha comenzado.
        self.sender().downloading()
    
    # SLOT. Este slot se ejecuta cuando el usuario solicita la descarga
    # de la página completa.
    def downloadPage(self):
        for tw in self.taskWidgets:
            job = tw.getJob()
            if job.state is not 'ready': continue
            
            self.jobDownloadManager.addJob(job)
            tw.downloading()
    
    # SLOT. Este slot se ejecuta cuando una de las tareas se ha descargado.
    # El JobDownloader es quien se encarga de descargar los ficheros y, por
    # tanto, de emitir la señal que ejecutará este slot.
    def jobDownloaded(self, job):
        for taskWidget in self.taskWidgets:
            if (taskWidget.getJob() == job):
                taskWidget.downloaded()
                break
    
    # SLOT.
    def openConfigDownloadDialog(self):
        dialog = ConfigDownloadDialog.ConfigDownloadDialog(self)
        
        if (dialog.exec_() == QDialog.Accepted):
            # Actualizar la configuración.
            self.loadConfig()
    
    # SLOT. El usuario solicita ver la siguiente página de trabajos.
    def nextPage(self):
        self.currentPage += 1
        self.updateNavButtons()
        self.loadJobs()
    
    # SLOT. El usuario solicita ver la anterior página de trabajos.
    def previousPage(self):
        self.currentPage -= 1
        self.updateNavButtons()
        self.loadJobs()
    
    def updateNavButtons(self):
        # Dependiendo de la página en la que se esté será necesario
        # activar o desactivar los botones de navegación. Si estamos
        # en la primera página, por ejemplo, se bloque el botón para
        # ir a la página anterior.
        if self.currentPage == 1: self.ui.previousButton.setEnabled(False)
        else: self.ui.previousButton.setEnabled(True)

        if self.currentPage == self.pages: self.ui.nextButton.setEnabled(False)
        else: self.ui.nextButton.setEnabled(True)
        
        self.setWindowTitle("Cola de trabajos (" + str(self.currentPage) + '/' + str(self.pages) + ')')
    
    # Cargar lista de trabajos.
    def loadJobs(self):
        # Cargar la lista de trabajos de la página actual.
        (jobs, hasNext) = volbrain.get_jobs_in_page(self.baseUrl, self.session, self.currentPage)
        
        
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
        folder = config.get('download', 'folder', fallback = os.getcwd())
        createSubfolder = config.getboolean('download', 'create_subfolder', fallback=True)
        
        # Configuración para saber qué ficheros descargar.
        downloadMni = config.getboolean('download', 'download_mni', fallback = True)
        downloadNat = config.getboolean('download', 'download_nat', fallback = True)
        downloadPdf = config.getboolean('download', 'download_pdf', fallback = True)
        
        
        self.jobDownloadManager.setConfig(folder, createSubfolder, downloadMni, downloadNat, downloadPdf)
        
    def closeEvent(self, event):
        self.reloadTimer.stop()
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
        
