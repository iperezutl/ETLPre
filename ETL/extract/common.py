#Importamos la librería de yaml
import yaml

#Definimos una variable global para guarar nuestra configuración
__config = None

#Verificamos si existe la configuración y si no la cargamos
def config():
    global __config
    if not __config:
        #Abrimos nuestro archivo yaml
        with open('config.yaml', mode='r') as f:
            #__config = yaml.load(f)
            __config = yaml.full_load(f)
            
    return __config
