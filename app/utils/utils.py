import os
from flask import current_app, abort, Response
def getPathFile(nameFile, section, folder):
    '''    Devuelve la ruta de la imagen'''
    carpeta_imagenes = os.path.join(current_app.root_path, section, folder)
    pathImage = os.path.join(carpeta_imagenes, nameFile)
    
    if not (os.path.isfile(pathImage)):
        return None
    
    return pathImage