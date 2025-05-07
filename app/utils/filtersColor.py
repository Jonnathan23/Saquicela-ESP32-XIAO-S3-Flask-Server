import cv2
import numpy as np
from app.bitwiseOperations import selectedOperation
import app.data.data as data

#* |----------| | Imagen/Video procesado | |----------|
def filterImplementationPartB (frame:np.ndarray) -> np.ndarray:
    """Funcion para aplicar ruido al video.
    Args:
        frame (numpy.ndarray): Imagen en escala de grises.        
    Returns:
        numpy.ndarray: Imagen total, con ruido generado."""
    
    height, width, channels = frame.shape     
    
    # Aplicar ruido gaussiano
    imageGaussianNoise = generateGaussianNoise(frame)
    
    # Aplicar ruido Speckle
    imageSpeckleNoise = generateSpeckleNoise(frame)         

    #* Crear imagen total -> original + ruido
    totalImage = np.full((height*2, width*2, channels), 0, dtype=np.uint8)    
    totalImage = np.zeros((height*2, width * 2, channels), dtype=np.uint8)    
    
    # Gausiano
    totalImage[:height, :width, :] = frame
    totalImage[:height, width:width*2, :] = imageGaussianNoise
    
    # Speckle
    totalImage[height:height*2, :width, :] = frame
    totalImage[height:height*2, width:width*2, :] = imageSpeckleNoise

    return totalImage

def implementFilterToImage (frame:np.ndarray) -> np.ndarray:
    """    Funcion para implementar filtros mediana, blur, Gaussiano, con mascara    """
    
    height, width, channels = frame.shape        

    # Mascara Central
    
    centerMask = createCenterMask(frame)

    imageWithMask = selectedOperation.get("OR")(frame, centerMask)

    # Mostrar mascara
    centerMask = cv2.cvtColor(centerMask, cv2.COLOR_BGR2RGB)    

    #* Crear imagen total -> original + filtros + deteccion_bordes
    totalImage = np.full((height, width*4, channels), 0, dtype=np.uint8)    
    totalImage = np.zeros((height, width * 4, channels), dtype=np.uint8)    
    
    # Mascara Central Rentangular AND
    totalImage[:height, :width, :] = frame
    totalImage[:height, width:width*2, :] = centerMask
    totalImage[:height, width*2:width*3, :] = imageWithMask
    
    
    return totalImage



#* |----------| | Filtros | |----------|
def filterMedia (frame) ->np.ndarray:
    '''Funcion para implementar el filtro media en una nueva imagen'''
    newImage = cv2.blur(
        src=frame,
        ksize=(data.kernel,data.kernel)
    )
    return newImage

def filterGaussian (frame, deviation=5) -> np.ndarray:
    smoothedImage = cv2.GaussianBlur(
        src=frame,
        ksize=(data.kernel,data.kernel),
        sigmaX=deviation
    )
    return smoothedImage

def filterBlur (frame) -> np.ndarray:
    src = frame.copy()
    blurImage = cv2.blur(
        src,
        ksize=(data.kernel,data.kernel)
    )
    return blurImage
    

#* |----------| | Mascaras | |----------|
def createCenterMask (frame: np.ndarray)-> np.ndarray:
    height, width = frame.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    
    x1, y1 = width//8, height//8
    x2, y2 = (width//8) + data.widthMask,( height//8) + data.heightMask
    cv2.rectangle(mask, (x1,y1), (x2,y2), 255, cv2.FILLED)
    
    return mask



#* |----------| | Ruido | |----------|
def generateGaussianNoise(frame:np.ndarray) -> np.ndarray:
    """Funcion para crear el ruido gaussiano.
    """
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



def generateSpeckleNoise (frame: np.ndarray) -> np.ndarray:
    """Funcion para crear el ruido de Speckle.
    """
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
    
    speckleNoise = np.random.normal(
        loc=data.media,
        scale=np.sqrt(data.variance),
        size=frame.shape
    ).astype(np.float32)
    
    noisy = imageFloat + imageFloat * speckleNoise
    noisy_clipped = np.clip(noisy, 0, 255).astype(np.uint8)
    return noisy_clipped
    
    