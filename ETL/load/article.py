#Importamos las clases que necesitamos de sqlalchemy
from sqlalchemy import Column, String, Integer
#Importamos el objeto Base
from base import Base
#Declaramso la clase Artículo que hereda a Base
class Article(Base):
    __tablename__ = 'articles'
    #Definición de columnas
    id = Column(String, primary_key=True)
    body = Column(String)
    host = Column(String)
    title = Column(String)
    newspaper_uid = Column(String)
    n_tokens_body = Column(Integer)
    n_tokens_title = Column(Integer)
    url = Column(String, unique=True)
    
    def __init__(self, uid, body, host, newspaper_uid, n_tokens_body, n_tokens_title, title, url):
        self.id = uid
        self.body = body
        self.host = host
        self.newspaper_uid = newspaper_uid
        self.n_tokens_title = n_tokens_title
        self.title = title
        self.url = url