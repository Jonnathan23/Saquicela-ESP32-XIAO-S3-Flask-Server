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
    
    height, width = grayImage.shape      
    
    # Extraer el fondo
    motion_mask = subtractBackground(grayImage,bg_subtractor)         

    #* Crear imagen total -> gris + ruido
    totalImage = np.full((height, width), 0, dtype=np.uint8)    
    totalImage = np.zeros((height, width * 2), dtype=np.uint8)
    totalImage[:, :width] = grayImage
    totalImage[:, width:] = motion_mask
    return totalImage


#* |----------| | Filtros| |----------|

def subtractBackground(grayImage:np.ndarray, bg_subtractor) -> np.ndarray:
    """Funcion para extraer el fondo."""
    motion_mask = bg_subtractor.apply(grayImage)
    return motion_mask



def implementNoise (grayImage) -> np.ndarray:
    """Funcion para crear el ruido.

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