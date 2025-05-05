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
    
    image_scaled = cv2.resize(grayImage,  dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    
    height, width = image_scaled.shape
    
    # Imagen ecualizada
    equalized_image = equalizeHistogram(image_scaled)
    
    # Extraer el fondo
    motion_mask = subtractBackground(image_scaled,bg_subtractor)         
    motion_mask_equalized = subtractBackground(equalized_image,bg_subtractor)         

    #* Crear imagen total -> gris + ruido
    totalImage = np.full((height, width), 0, dtype=np.uint8)    
    totalImage = np.zeros((height, width * 4), dtype=np.uint8)
#    totalImage[:, :width] = image_scaled
#    totalImage[:, width:width*2] = equalized_image
#    totalImage[:, width*2:width*3] = motion_mask_equalized
#    totalImage[:, width*3:width*4] = motion_mask
    
    totalImage[:, :width] = image_scaled
    totalImage[:, width:width*2] = motion_mask
    totalImage[:, width*2:width*3] = equalized_image
    totalImage[:, width*3:width*4] = motion_mask_equalized
    
    return totalImage


def filterImplementation_part_b (frame:np.ndarray) -> np.ndarray:
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