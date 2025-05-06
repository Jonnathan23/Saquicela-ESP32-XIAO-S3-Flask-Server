import cv2
import numpy as np
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

    #* Crear imagen total -> original + filtros
    totalImage = np.full((height*2, width*3, channels), 0, dtype=np.uint8)    
    totalImage = np.zeros((height*2, width * 3, channels), dtype=np.uint8)    
    
    # Gausiano
    totalImage[:height, :width, :] = frame
    totalImage[:height, width:width*2, :] = frame
    
    # Media
    totalImage[height:height*2, :width, :] = frame
    totalImage[height:height*2, width:width*2, :] = frame
    
    return totalImage



#* |----------| | Filtros | |----------|
def filterMedia (frame,width, height) ->np.ndarray:
    '''Funcion para implementar el filtro media en una nueva imagen'''
    imageMedia = frame.copy()
    newImage = cv2.blur(
        src=imageMedia,
        ksize=(width, height)
    )
    return newImage

def filterGaussian (frame, width, height, deviation) -> np.ndarray:
    imageGaussian = frame.copy()
    smoothedImage = cv2.GaussianBlur(
        src=imageGaussian,
        ksize=(width,height),
        sigmaX=deviation
    )
    return smoothedImage

#* |----------| | Mascaras | |----------|
def createCenterMask (frame: np.ndarray)-> np.ndarray:
    height, width = frame.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    
    x1, y1 = width//4, height//4
    x2, y2 = 3*width//4, 3*height//4
    cv2.rectangle(mask, (x1,y1), (x2,y2), 255, cv2.FILLED)



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
    
    