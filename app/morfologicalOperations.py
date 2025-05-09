
#* |----------| | Renderizaciones de imagenes| |----------|

import cv2
import numpy as np
import app.data.data as data

def erosionOperation (image:np.ndarray):
    kernel = data.morfologicalKernel
    structuringElement = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (kernel, kernel)
    )
    
    erodedImage = cv2.erode(
        src=image,
        kernel=structuringElement,
        iterations=1
    )
    
    return erodedImage

def dilatationOperation(image: np.ndarray) -> np.ndarray:
    """
    Dilata la imagen, expandiendo las zonas brillantes.
    """
    kernelSize = data.morfologicalKernel
    structuringElement = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (kernelSize, kernelSize)
    )
    dilatedImage = cv2.dilate(
        src=image,
        kernel=structuringElement,
        iterations=1
    )
    return dilatedImage

def topHatOperation(image: np.ndarray) -> np.ndarray:
    """
    Top-Hat = imagen original − apertura.
    Resalta pequeñas regiones brillantes sobre fondo oscuro.
    """
    kernelSize = data.morfologicalKernel
    structuringElement = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (kernelSize, kernelSize)
    )
    topHatImage = cv2.morphologyEx(
        src=image,
        op=cv2.MORPH_TOPHAT,
        kernel=structuringElement
    )
    return topHatImage

def blackHatOperation(image: np.ndarray) -> np.ndarray:
    """
    Black-Hat = cierre − imagen original.
    Resalta pequeñas regiones oscuras sobre fondo brillante.
    """
    kernelSize = data.morfologicalKernel
    structuringElement = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (kernelSize, kernelSize)
    )
    blackHatImage = cv2.morphologyEx(
        src=image,
        op=cv2.MORPH_BLACKHAT,
        kernel=structuringElement
    )
    return blackHatImage

def originalImageTopBlackHatOperation(original: np.ndarray):
    '''originaln Original + (Top Hat – Black Hat'''
    topHat = topHatOperation(original)
    blackHat = blackHatOperation(original)
    rest = cv2.subtract(topHat, blackHat)
    imageTotal = cv2.add(original, rest)
    
    return imageTotal
    

morfologicalOperationsSelect = {
    data.TypeMorfologicalOperations.erosion: erosionOperation,
    data.TypeMorfologicalOperations.dilatation: dilatationOperation,
    data.TypeMorfologicalOperations.topHat: topHatOperation,
    data.TypeMorfologicalOperations.blackHat: blackHatOperation,
    data.TypeMorfologicalOperations.originalImageTopBlackHat: originalImageTopBlackHatOperation
}