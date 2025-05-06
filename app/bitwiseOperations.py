import cv2
import numpy as np

def andOperation (frame:np.ndarray, mask:np.ndarray) -> np.ndarray:
    """Funcion para aplicar la operacion AND entre una imagen y una mascara."""
    totalImage = cv2.bitwise_and(frame, mask)
    return totalImage

def orOperation (frame:np.ndarray, mask:np.ndarray) -> np.ndarray:
    """Funcion para aplicar la operacion OR entre una imagen y una mascara."""
    totalImage = cv2.bitwise_or(frame, mask)
    return totalImage

def xorOperation (frame:np.ndarray, mask:np.ndarray) -> np.ndarray:
    """Funcion para aplicar la operacion XOR entre una imagen y una mascara."""
    totalImage = cv2.bitwise_xor(frame, mask)
    return totalImage
