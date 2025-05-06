import cv2
import numpy as np

def filterImplementationPartB (frame:np.ndarray) -> np.ndarray:
    """Funcion para aplicar los filtros morfológicos.
    Args:
        frame (numpy.ndarray): Imagen en escala de grises.        
        bg_subtractor (cv2.BackgroundSubtractorMOG2): Objeto para extraer el fondo.
    Returns:
        numpy.ndarray: Imagen total, con filtros aplicados."""
    
    height, width, channels = frame.shape     
    
         

    #* Crear imagen total -> gris + ruido
    totalImage = np.full((height, width, channels), 0, dtype=np.uint8)    
    totalImage = np.zeros((height, width * 2, channels), dtype=np.uint8)
    totalImage[:height, :width, :] = frame

    return totalImage
