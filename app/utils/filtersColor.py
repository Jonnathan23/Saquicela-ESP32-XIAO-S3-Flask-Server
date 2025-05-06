import cv2
import numpy as np
import app.data.data as data

def filterImplementationPartB (frame:np.ndarray) -> np.ndarray:
    """Funcion para aplicar los filtros morfológicos.
    Args:
        frame (numpy.ndarray): Imagen en escala de grises.        
        bg_subtractor (cv2.BackgroundSubtractorMOG2): Objeto para extraer el fondo.
    Returns:
        numpy.ndarray: Imagen total, con filtros aplicados."""
    
    height, width, channels = frame.shape     
    
    # Aplicar ruido gaussiano
    imageGaussianNoise = generateGaussianNoise(frame)
         

    #* Crear imagen total -> original + ruido + solucion
    totalImage = np.full((height, width, channels), 0, dtype=np.uint8)    
    totalImage = np.zeros((height, width * 2, channels), dtype=np.uint8)
    
    # Gausiano
    totalImage[:height, :width, :] = frame
    totalImage[:height, width:width*2, :] = imageGaussianNoise

    return totalImage

def generateGaussianNoise(frame):
    if(data.media == 0 or data.deviation == 0 or data.variance == 0):        
        frameWithOutline = frame.copy()
        cv2.putText(frameWithOutline,
                    f"Sin implementar ruido",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,            # escala de letra
                    255,          # color blanco en gris
                    2,            # grosor
                    cv2.LINE_AA)
        return frameWithOutline
    
    imageFloat = frame.copy()
    imageFloat = imageFloat.astype(np.float32)
    gaussNoise = np.random.normal(
        loc=data.media,
        scale=data.deviation,
        size=imageFloat.shape    
    ).astype(np.float32)
    
    noisy = imageFloat + gaussNoise
    noisy = np.clip(noisy, 0, 255)
    imageWithNoise = noisy.astype(np.uint8)
    
    return imageWithNoise