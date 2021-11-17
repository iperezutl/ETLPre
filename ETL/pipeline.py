#Importamos la libreria logging para mostrar mensajes en la consola.
import logging
#Aplicamos la configuración básica al logging
logging.basicConfig(level = logging.INFO)
import subprocess
import datetime

logger = logging.getLogger(__name__)
news_sites_uids = ['elpais']

def main():
    _extract()
    _transform()
    _load()
    logger.info('Proceso ETL finalizado')


def _extract():
    logger.info('Iniciando el proceso de extracción')
    
    #Iteramos en cada uno de los newssites que tenemos.
    for news_site_uid in news_sites_uids:
        #Corremos un subproceso para ejecutar el primer programa en la carpeta /extract
        subprocess.run(['python', 'main.py', news_site_uid], cwd='./extract')
        
        #Movemos los archivos generados al directorio transform
        #Linux
        #subprocess.run(['find', '.', '-name', '{}*'.format(news_sites_uid), 'exec', 'mv', '{}', 
        #    '../transform/{}_.csv'.format(news_sites_uid), ';'], cwd='./extract')
        
        #Windows
        subprocess.run(['move', r'extract\*.csv', r'transform'], shell=True)

def _transform():
    logger.info('Iniciando el proceso de transformación')
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    
    #Iteramos en cada uno de los newssites que tenemos.
    for news_site_uid in news_sites_uids:
        #Linux
        #dirty_data_filename = '{}_.csv'.format(news_site_uid)
        #clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        #subprocess.run(['pyton', 'main.py', dirty_data_filename], cwd='./transform')
        #subprocess.run(['rm', dirty_data_filename], cwd='./transform')
        #subprocess.run(['mv', clean_data_filename, './load/{}.csv'.format(news_site_uid)], cwd='./transform')
        
        #windows
        dirty_data_filename = '{}_{datetime}_articles.csv'.format(news_site_uid, datetime=now)
        #Corremos un subproceso para ejecutar el segundo programa en la carpeta /transform
        subprocess.run(['python', 'main.py', dirty_data_filename], cwd='./transform')
        subprocess.run(['del', dirty_data_filename], shell=True, cwd='./transform')      
        subprocess.run(['move', r'transform\*.csv', r'load'], shell=True)
        
def _load():
    logger.info('Iniciando el proceso de carga')
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    
    for news_site_uid in news_sites_uids:
        #Linux
        #clean_data_file_name = '{}.csv'.format(news_site_uid)
        #subprocess.run(['python', 'main.py', clean_data_file_name], cwd='./load')
        #subprocess.run(['rm', clean_data_file_name], cwd='./load')

        #Windows
        clean_data_filename = 'clean_{}_{datetime}_articles.csv'.format(news_site_uid, datetime=now)
        #Corremos un subproceso para ejecutar el tercer programa en la carpeta /extract
        subprocess.run(['python', 'main.py', clean_data_filename], cwd='./load')
        subprocess.run(['del', clean_data_filename], shell=True, cwd='./load')
        
if __name__ == '__main__':
    main()