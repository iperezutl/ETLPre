#Importamos la librería argparse para generar un cli
import argparse
#Importamos las librerías csv y datetime
import csv
import datetime
#Importamos la libreria loggin para mostrar cosas en la consola mejor que print.
import logging
from os import write
import requests

from requests.models import HTTPError
logging.basicConfig(level=logging.INFO)
#Importamos el módulo de expresiones regulares
import re

#Importamos los errores
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError


#Cargamos los news_page_objects con un alias
import news_page_objects as news
#Importamos la variable de configuración
from common import config

#Obtenemos una referencia a nuestro logger.
logger = logging.getLogger(__name__)
#Definiendo las expresiones regulares para los links
is_well_formed_link = re.compile(r'^https?://.+/.+$')#https://example.com/hello
is_root_path = re.compile(r'^/.+$') #/some-text


#Método para recuperar las url's de los sitios de noticias guardados en la configuración
def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    
    logging.info('Iniciando el scrapper for {}'.format(host))
    #Recuperamos la lista de noticias el homepage
    homepage = news.HomePage(news_site_uid, host)
    
    articles = []
    #Recorremos la lista de enlaces para poder extrar su contenido
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)
        
        if article:
            logger.info('Artículo obtenido!!')
            articles.append(article)
            print(article.title)
            #break
            
    _save_articles(news_site_uid, articles)
    print('Num. Artículos' + str(len(articles)))

#Función para guardar los artículos en un archivo csv
def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site_uid}_{fdatetime}_articles.csv'.format(
        news_site_uid = news_site_uid, fdatetime=now)
    csv_headers = list(filter(lambda property: not property.startswith('_'),
                    dir(articles[0])))
    
    #Escribimos en el archivo.
    with open(out_file_name, mode='w+', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        
        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)
    
#Método que recupera la información del artículo.
def _fetch_article(news_site_uid, host, link):
    logger.info('Recuperando el artículo de: {}'.format(link))
    
    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error mientras se obteniía el artículo.', exc_info=False)
    
    if article and not article.body:
        logger.warning('Artículo Inválido. No hay cuerpo')
        return None
    
    return article
    

#Método que comprueba que los enlaces están bien formados.
def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)

if __name__ == '__main__':
    #Creamos un nuevo parser
    parser = argparse.ArgumentParser()
    
    #Recuperamos las claves que se definieron en el archivo de configuración convirtiendolo a lista
    news_site_choices = list(config()['news_sites'].keys())
    
    #Añadiendo argumentos (obligatorios) y ayuda al parser
    parser.add_argument('news_site',
                        help='El sitio de noticias que quieres escrapear',
                        type=str,
                        choices=news_site_choices)
    #Parsea los argumentos y nos de un objeto con ellos.
    args = parser.parse_args()
    #Llamamos a la función para recuperar las url's
    _news_scraper(args.news_site)
    