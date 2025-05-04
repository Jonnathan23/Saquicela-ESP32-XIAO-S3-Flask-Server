import cv2
import requests
import numpy as np
from io import BytesIO

def filterImplementation (grayImage):
    """Funcion para aplicar los filtros morfológicos.

    Args:
        grayImage (numpy.ndarray): Imagen en escala de grises.

    Returns:
        numpy.ndarray: Imagen total, con filtros aplicados."""
    
    height, width = grayImage.shape
    # Crear ruido
    noise_image = implementNoise(grayImage) # Imagen en escala de grises + runois

    # Crear imagen total -> gris + ruido
    totalImage = np.full((height, width), 0, dtype=np.uint8)    
    totalImage = np.zeros((height, width * 2), dtype=np.uint8)
    totalImage[:, :width] = grayImage
    totalImage[:, width:] = noise_image
    return totalImage


def implementNoise (grayImage):
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