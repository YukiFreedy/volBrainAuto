# -*- coding: utf-8 -*-

import sys
import os
import re

import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import urllib

'''
CLASE JOB
Clase para representar los trabajos: archivos que
se han subido y están procesados o están siendo procesados.
ATRIBUTOS:
    -filename: nombre del fichero
    -date:     fecha de subida
    -state:    ready_to_launch -> está subido pero todavía no se está procesando.
               launched -> se está procesando
               ready -> ya se ha procesado. Los ficheros ya se podrán descargar.
    -links:		 array con los enlaces de descarga (tres elementos).
               
'''
class Job:
    def __init__(self, job_id, filename, date, state, links):
        self.job_id = job_id
        self.filename = filename
        self.date = date
        self.state = state
        self.links = links
    def __eq__(self, other_job):
        return other_job.job_id == self.job_id


'''
CLASE LOGINEXCEPTION
Excepción para representar el error durante el inicio de sesión.
'''
class LoginException(Exception):
    pass




'''
Inicia sesión en la web.

@param base_url Url de volBrain.
@param email    Email del usuario
@param password Contraseña.

@return Devuelve un objeto Session sobre el que se
        harán las siguientes peticiones al servidor.
'''
def login(base_url, email, password):
    payload = {'email': email, 'password': password}
    
    session = requests.Session()
    
    r = session.post(base_url + 'login.php', payload)
    
    c = r.content
    soup = BeautifulSoup(c, "lxml")

    form = soup.find(id="upload_form")
    
    # Si en la página no hay un formulario significa que
    # el login no ha ido bien.    
    if form is None: raise LoginException()
    
    # Se devuelve el objeto session para poder lanzar nuevas
    # peticiones desde fuera de la función.
    return session


'''
Obtiene el listado de ficheros en una página.

@param base_url Url de volBrain
@param session Objeto Session devuelto por login()
@param return Devuelve una tupla en la que el primer elemento
                es un array de instancias de Job y el segundo
                es un boolean que valdrá True si hay otra página
                de resultados.
'''
def get_jobs_in_page(base_url, session, page = 1):
    jobs = []
    
    # Aunque la tabla con la lista de ficheros aparece en 
    # la página members.php, esta tabla es cargada vía
    # ajax (con Javascript). Eso quiere decir que, al momento
    # de hacer la petición a members.php esa tabla todavía no
    # está cargada y no se encontrará en el DOM.
    # Por tanto, la petición se hará a ajax_jobs_list.php
    # que es la página que contiene verdaderamente la tabla.
    
    r = session.get(base_url + 'ajax_jobs_list.php?p=' + str(page))
    
    soup = BeautifulSoup(r.content, "lxml")

    # Algunos de los tr representan archivos subidos, otros
    # pueden ser la cabecera o el pie de la tabla (habrá que filtrarlos).
    trs = soup.find_all('tr')
    
    # Cantidad de ficheros subidos/procesándose =
    # número de filas en la tabla menos la fila que se usa de
    # cabecera y las tres que se usan de pie.
    jobs_in_page = len(trs) - 1 - 3
    
    # Para cada uno de los trabajos...
    for i in range(0, jobs_in_page):
        tds = trs[i + 1].find_all('td')
        
        job_id = tds[0].string.strip()
        filename = tds[1].string.strip()
        date = tds[2].string.strip()
        
        job_id.strip()
        
        state = 'unknown'
        
        # Se conoce el estado del trabajo a partir de la imagen
        # que aparece.
        if tds[3].find('img', {'src': 'img/job_ready.png'}) is not None:
            state = 'ready_to_launch'
        elif tds[3].find('img', {'src': 'img/job_launched.png'}) is not None:
            state = 'launched'
        elif tds[3].find('img', {'src': 'img/job_deleted.png'}) is not None:
            state = 'deleted'
        else:
            state = 'ready'
        
        # Si el trabajo está listo habrá que descubrir los enlaces
        # de descarga de los ficheros.
        links = []
        if state == 'ready':
            lks = tds[3].find_all('a')
            links += [lks[0]['href'], lks[1]['href'], lks[2]['href']]
        
        jobs += [Job(job_id, filename, date, state, links)]
    
    # Se averigua si hay una siguiente página.
    hasNext = soup.find('span', {'onclick': 'javascript:loadJobList(' + str(page + 1) +');'}) is not None
    
    return (jobs, hasNext)

'''
Devuelve todos los trabajos. Para ello recorre todas las páginas
de resultados.
'''
def get_all_jobs(base_url, session):
    current_page = 1
    (jobs, hasNext) = get_jobs_in_page(base_url, session, current_page)
    
    while hasNext == True:
        current_page += 1
        (j, hasNext) = get_jobs_in_page(base_url, session, current_page)
        jobs += j
        
    return jobs

'''
Devuelve el número de páginas.
'''
def count_pages(base_url, session):
    r = session.get(base_url + 'ajax_jobs_list.php')
    
    soup = BeautifulSoup(r.content, "lxml")

    spans = soup.find_all('span', {'style' : 'color:blue;cursor:pointer;cursor:hand;'})
    
    if len(spans) == 0: return 1
    
    # Se busca en el último span, que se corresponde con el
    # enlace a la última página, y se busca en el atributo
    # onclick el número de la página.
    onclick = spans[len(spans) - 1]['onclick']
    
    p = re.compile('javascript:loadJobList\((.+)\).*')
    
    return int(p.search(onclick).group(1))
     

'''
Dado un trabajo, descarga sus ficheros si es posible.
@param job Trabajo (instancia de Job).
@param folder Optativo. Carpeta de destino.
@param create_subfolder Optativo. Si es True se creará una nueva carpeta para este trabajo.
'''
def download_job_files(job, folder = None, create_subfolder = True, downloadMni = True, downloadNat = True, downloadPdf = True):
    
    # Se comprueba si la descarga está lista.
    if job.state is not 'ready': return
    
    # La carpeta de destino, por defecto, es la carpeta
    # donde se ejecuta el script.
    if folder is None: folder = './'
    
    # El usuario puede establecer si crear una subcarpeta por
    # cada trabajo o si prefiere meter todos los ficheros en
    # la misma carpeta.
    if create_subfolder:
        folder += 'job_' + job.job_id + '/'

    if not os.path.exists(folder):
        os.makedirs(folder)
    
    if downloadMni: urllib.request.urlretrieve(job.links[0], folder + 'mni' + job.job_id +'.zip')
    if downloadNat: urllib.request.urlretrieve(job.links[1], folder + 'nat' + job.job_id +'.zip')
    if downloadPdf: urllib.request.urlretrieve(job.links[2], folder + 'pdf' + job.job_id +'.pdf')


    
