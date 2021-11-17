#Importamos la librería argparse para parsear argumentos de CLI
import argparse
#Importamos la librería logging para mostrar mensajes en consola
import logging
#Hacemos la configuración básica
logging.basicConfig(level=logging.INFO)

#Importamos la librería de pandas
import pandas as pd
#Importamos la clase Article 
from article import Article
#Improtamos los objetos de base
from base import Base, engine, Session

#Obtenemos una referencia al logger
logger = logging.getLogger(__name__)

#Definición del la función main
def main(filename):
    #Generamos el squema de la BD.
    Base.metadata.create_all(engine)
    #Iniciamos sesión
    session = Session()
    #Leemos nuestro archivo csv
    articles = pd.read_csv(filename, encoding='utf-8')
    
    #Iteramos entre las filas de csv mediante el método iterrows() y vamos cargando
    #los articulos a la base de datos.
    for index, row in articles.iterrows():
        logger.info('Cargando el artículo con uid: {} en la BD'.format(row['uid']))
        article = Article(row['uid'],
                          row['body'],
                          row['host'],
                          row['newspaper_uid'],
                          row['n_tokens_body'],
                          row['n_tokens_title'],
                          row['title'],
                          row['url'])
        session.add(article)
        
        session.commit()
        session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #Creamos el argumento filename
    parser.add_argument('filename',
                        help='El archivo que deseas cargar hacia la BD',
                        type=str)
    
    args = parser.parse_args()
    
    main(args.filename)
