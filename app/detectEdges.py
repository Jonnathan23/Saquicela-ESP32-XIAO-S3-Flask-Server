import cv2
import numpy as np

import app.data.data as data
#* |----------| | Deteccion de bordes | |----------|

def detectEdgesCanny(frame: np.ndarray, threshold1: int = 40, threshold2: int = 80):
    '''Funcion para deteccion de bordes por Canny'''
    
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if frame.ndim == 3 else frame.copy()
    kernelValue = 7 if data.kernel >= 7 else 3
    
    edges = cv2.Canny(
        image=grayImage,
        threshold1=threshold1,
        threshold2=threshold2,
        apertureSize=3,
        L2gradient=False
    )
    
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def detectEdgesSobel(frame: np.ndarray) -> np.ndarray:
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if frame.ndim == 3 else frame.copy()
    
    # Gradientes
    gradX = cv2.Sobel(
        src=grayImage,
        ddepth=cv2.CV_64F,
        dx=1, dy=0,
        ksize=data.kernel
    )
    gradY = cv2.Sobel(
        src=grayImage,
        ddepth=cv2.CV_64F,
        dx=0, dy=1,
        ksize=data.kernel
    )
    
    # Valores absolutos y a uint8
    absGradX = cv2.convertScaleAbs(gradX)
    absGradY = cv2.convertScaleAbs(gradY)
    
    # Combinar ambos gradientes
    sobelCombined = cv2.addWeighted(
        src1=absGradX, alpha=0.5,
        src2=absGradY, beta=0.5,
        gamma=0
    )
    
    return cv2.cvtColor(sobelCombined, cv2.COLOR_GRAY2BGR)

edges = {
    data.TypeBordersOptions.canny: detectEdgesCanny,
    data.TypeBordersOptions.sobel: detectEdgesSobel
}