import argparse
import csv
import sys
import time
import os

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
               
'''
Job = namedtuple("MyStruct", "job_id filename date state links")




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
    if form is None: raise exception('Login not correct.')
    
    # Se devuelve el objeto session para poder lanzar nuevas
    # peticiones desde fuera de la función.
    return session


'''
Obtiene el listado de ficheros.

@param base_url Url de volBrain
@param session Objeto Session devuelto por login()
@param return Array de instancias de Job.
'''
def get_job_list(base_url, session):
    jobs = []
    
    # Aunque la tabla con la lista de ficheros aparece en 
    # la página members.php, esta tabla es cargada vía
    # ajax (con Javascript). Eso quiere decir que, al momento
    # de hacer la petición a members.php esa tabla todavía no
    # está cargada y no se encontrará en el DOM.
    # Por tanto, la petición se hará a ajax_jobs_list.php
    # que es la tabla que contiene verdaderamente la tabla.
    
    r = session.get(base_url + 'ajax_jobs_list.php')
    
    # La página members.php tiene un div con id =  job_list.
    # Ese div contiene una tabla. Algunas de las filas de esa
    # tabla representan los trabajos. Algunos de ellos estarán
    # procesados y otros no.
    #print(r.content)
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
        else:
            state = 'ready'
        
        # Si el trabajo está listo habrá que descubrir los enlaces
        # de descarga de los ficheros.
        links = []
        if state == 'ready':
            lks = tds[3].find_all('a')
            links += [lks[0]['href'], lks[1]['href'], lks[2]['href']]
        
        jobs += [Job(job_id, filename, date, state, links)]
    
    return jobs

'''
Dado un trabajo, descarga sus ficheros si es posible.
@param job Trabajo (instancia de Job).
@param folder Optativo. Carpeta de destino.
@param create_subfolder Optativo. Si es True se creará una nueva carpeta para este trabajo.
'''
def download_job_files(job, folder = None, create_subfolder = True):
    
    # Se comprueba si la descarga está lista.
    if job.state is not 'ready' return
    
    # La carpeta de destino, por defecto, es la carpeta
    # donde se ejecuta el script.
    if folder is None: folder = './'
    
    # El usuario puede establecer si crear una subcarpeta por
    # cada trabajo o si prefiere meter todos los ficheros en
    # la misma carpeta.
    if create_subfolder:
        folder += 'job_' + job.job_id

    if not os.path.exists(folder):
        os.makedirs(folder)
      
    urllib.request.urlretrieve(job.links[0], folder + 'mni' + job.job_id +'.zip')
    urllib.request.urlretrieve(job.links[1], folder + 'nat' + job.job_id +'.zip')
    urllib.request.urlretrieve(job.links[2], folder + 'pdf' + job.job_id +'.pdf')





#############################
###  PROGRAMA DE PRUEBA  ####
#############################
def main():
    print("volBrain")
    session = None
    base_url = 'http://volbrain.upv.es/'
    
    try:
        #session = login(base_url, 'vicrivaz@inf.upv.es', '09081996')
        session = login(base_url, 'rafaelspam1234@gmail.com', 'rafaelspam')
        
        jobs = get_job_list(base_url, session)
        
        print('Jobs: ', len(jobs))
        for job in jobs:
            print("'", "'", job.job_id, "'", job.filename, " ", job.date, " ", job.state)
            for link in job.links:
                print('\t', link)
        
        download_job_files(jobs[0], create_subfolder = False)      
    except LoginException:
        print("Login error.")
        exit()
    
    
    

if __name__ == '__main__':
    main()

    
