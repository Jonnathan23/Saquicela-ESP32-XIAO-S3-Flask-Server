import cv2
from flask import abort, Response


from app.morfologicalOperations import morfologicalOperationsSelect

from app.utils.utils import getPathFile
import app.data.data as data

def renderImageAxialBoneC (urlImage):
    
    pathImageAxialBoneC = getPathFile(urlImage, "static", "images")
    
    if(pathImageAxialBoneC == None):
        return
    
    grayImage = cv2.imread(pathImageAxialBoneC, cv2.IMREAD_GRAYSCALE)
    if grayImage is None:
       abort(500, "Error al leer la imagen con OpenCV")
    
    imageProcessed = morfologicalOperationsSelect[data.morfologicalOperation](grayImage)
       
    success, buffer = cv2.imencode(".jpg", imageProcessed)
    if not success:
        abort(500, "Error al codificar la imagen procesada")
        
    imagenBytes = buffer.tobytes()
    
    return Response(imagenBytes, mimetype="image/jpeg")
