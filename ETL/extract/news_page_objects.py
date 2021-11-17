#Importamos la libreria BeautifulSoup
import bs4
#Importamos la libreria request
import requests
from common import config

#Creamos una clase que representa la página de noticias
class NewsPage:
    def __init__(self, news_site_uid, url):
        #Obtenemos una referencia a la configuración.
        self._config = config()['news_sites'][news_site_uid]
        #Obtenemos las queries guardadas en la cofiguración.
        self._queries = self._config['queries']
        #Objeto con el parse html de bs4
        self._html = None
        
        #Invocamos al método visit
        self._visit(url)
        
    #Método para ejecutar una consulta en el árbol html
    def _select(self, query_string):
        return self._html.select(query_string)
    
    #Método para consultar la página de noticias que solicitamos
    def _visit(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

#Creamos una clase que representa la página pincipal de la web con base en NewsPage
class HomePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
    
    
    #Definimos una propiedad que contiene la lista de enlaces recuperados en la consulta
    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)
        #Retornamos la lista evitando repetidos
        return set(link['href'] for link in link_list)

#Creamos una clase que representa la página con la información del artículo con base en NewPage
class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        self._url = url
        super().__init__(news_site_uid, url)
     
    #Definimos una propiedad que contiene el cuerpo del artítulo   
    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''
    
    #Definimos una propiedad que contiene el título del artítulo   
    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''
    
    #Definimos una propiedad que contiene la url del artítulo   
    @property
    def url(self):
        return self._url