import cv2
import numpy as np

#* |----------| | Imagenes totales | |----------|

def filterImplementation_part_a (grayImage:np.ndarray , bg_subtractor) -> np.ndarray:
    """Funcion para aplicar los filtros morfológicos.
    Args:
        grayImage (numpy.ndarray): Imagen en escala de grises.        
        bg_subtractor (cv2.BackgroundSubtractorMOG2): Objeto para extraer el fondo.
    Returns:
        numpy.ndarray: Imagen total, con filtros aplicados."""
    
    imageScaled = cv2.resize(grayImage,  dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    
    height, width = imageScaled.shape
    
    # Imagen ecualizada
    equalizedHistogramImage = equalizeHistogram(imageScaled)
    equalizedCLAHEImage = methodCLAHE(imageScaled)
    
    # Extraer el fondo
    motionMask = subtractBackground(imageScaled,bg_subtractor)         
    motionMaskEqualizedHistogram = subtractBackground(equalizedHistogramImage,bg_subtractor)    
    motionMaskEqualizedCLAHE = subtractBackground(equalizedCLAHEImage,bg_subtractor)     

    #* Crear imagen total -> gris + ruido
    totalImage = np.full((height*2, width*4), 0, dtype=np.uint8)    
    totalImage = np.zeros((height*2, width * 4), dtype=np.uint8)
    
    #Imagen original
    totalImage[:height, :width] = imageScaled
    totalImage[:height, width:width*2] = motionMask
    
    #Imagen ecualizada por histograma
    totalImage[:height, width*2:width*3] = equalizedHistogramImage
    totalImage[:height, width*3:width*4] = motionMaskEqualizedHistogram
    
    #Imagen ecualizada por CLAHE
    totalImage[height:height*2, :width] = equalizedCLAHEImage
    totalImage[height:height*2, width:width*2] = motionMaskEqualizedCLAHE
    
    return totalImage


def filterImplementationPartB (frame:np.ndarray) -> np.ndarray:
    """Funcion para aplicar los filtros morfológicos.
    Args:
        frame (numpy.ndarray): Imagen en escala de grises.        
        bg_subtractor (cv2.BackgroundSubtractorMOG2): Objeto para extraer el fondo.
    Returns:
        numpy.ndarray: Imagen total, con filtros aplicados."""
    
    height, width = frame.shape     
    
         

    #* Crear imagen total -> gris + ruido
    totalImage = np.full((height, width), 0, dtype=np.uint8)    
    totalImage = np.zeros((height, width * 2), dtype=np.uint8)
    totalImage[:, :width] = frame

    return totalImage


#* |----------| | Filtros| |----------|

def subtractBackground(grayImage:np.ndarray, bg_subtractor) -> np.ndarray:
    """Funcion para extraer el fondo."""
    motion_mask = bg_subtractor.apply(grayImage)
    return motion_mask


# |----------| | Iliminacion| |----------|
def equalizeHistogram (grayImage) -> np.ndarray:
    """Funcion para equalizar el histograma."""
    equalized_image = cv2.equalizeHist(grayImage)
    return equalized_image

def methodCLAHE (grayImage) -> np.ndarray:
    """Funcion para equalizar el histograma."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    equalized_image = clahe.apply(grayImage)
    return equalized_image



# |----------| | Ruido| |----------|

def implementNoiseSaltPepper (grayImage) -> np.ndarray:
    """Funcion para crear el ruido de sal y pimienta.

    Args:
        grayImage (numpy.ndarray): Imagen en escala de grises.

    Returns:
        numpy.ndarray: Imagen en escala de grises con ruido."""
    # Crear ruido
    N = 537
    height, width = grayImage.shape
    noise = np.full((height, width), 0, dtype=np.uint8)
    random_positions = (np.random.randint(0, height, N), np.random.randint(0, width, N))
                
    noise[random_positions[0], random_positions[1]] = 255
    noise_image = cv2.bitwise_or(grayImage, noise)
    return noise_image