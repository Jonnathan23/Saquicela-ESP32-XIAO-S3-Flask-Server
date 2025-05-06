import cv2
import numpy as np

from app.data.backgroundSubtractor import background_subtractor_original
from app.data.backgroundSubtractor import background_subtractor_histogram
from app.data.backgroundSubtractor import background_subtractor_clahe
from app.bitwiseOperations import orOperation, xorOperation, andOperation

#* |----------| | Imagenes totales | |----------|

def filterImplementation_part_a (grayImage:np.ndarray) -> np.ndarray:
    """Funcion para aplicar los filtros morfológicos.
    Args:
        grayImage (numpy.ndarray): Imagen en escala de grises.        
        bg_subtractor (cv2.BackgroundSubtractorMOG2): Objeto para extraer el fondo.
    Returns:
        numpy.ndarray: Imagen total, con filtros aplicados."""
    
    # grayImage = cv2.resize(grayImage,  dsize=None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    
    height, width = grayImage.shape
    
    #smoothedImgage = cv2.GaussianBlur(grayImage, (11, 11), 0)
    
    # Imagen ecualizada
    equalizedHistogramImage = equalizeHistogram(grayImage)
    equalizedCLAHEImage = methodCLAHE(grayImage)
    
    # Extraer el fondo    
    motionMask = subtractBackground(grayImage,background_subtractor_original)         
    motionMaskEqualizedHistogram = subtractBackground(equalizedHistogramImage,background_subtractor_histogram)    
    motionMaskEqualizedCLAHE = subtractBackground(equalizedCLAHEImage,background_subtractor_clahe)     

    # Resultado de bitwise_operations AND
    totalOriginalImageAND = andOperation(grayImage, motionMask)
    totalHistogramImageAND = andOperation(equalizedHistogramImage, motionMask)
    totalCLAHEImageAND = andOperation(equalizedCLAHEImage, motionMask)
    
    # Resultado de bitwise_operations OR
    totalOriginalImageOR = orOperation(grayImage, motionMask)
    totalHistogramImageOR = orOperation(equalizedHistogramImage, motionMaskEqualizedHistogram)
    totalCLAHEImageOR = orOperation(equalizedCLAHEImage, motionMaskEqualizedCLAHE)
    
    # Resultado de bitwise_operations XOR    
    totalOriginalImageXOR = xorOperation(grayImage, motionMask)
    totalHistogramImageXOR = xorOperation(equalizedHistogramImage, motionMaskEqualizedHistogram)
    totalCLAHEImageXOR = xorOperation(equalizedCLAHEImage, motionMaskEqualizedCLAHE)


    #* Crear imagen total -> gris + mascara + bitwise_operations
    totalImage = np.full((height*3, width*5), 0, dtype=np.uint8)    
    totalImage = np.zeros((height*3, width *5), dtype=np.uint8)
    
    #Imagen original
    totalImage[:height, :width] = grayImage
    totalImage[:height, width:width*2] = motionMask
    totalImage[:height, width*2:width*3] = totalOriginalImageAND
    totalImage[:height, width*3:width*4] = totalOriginalImageOR
    totalImage[:height, width*4:width*5] = totalOriginalImageXOR
    
    
    #Imagen ecualizada por CLAHE
    totalImage[height:height*2, :width] = equalizedCLAHEImage
    totalImage[height:height*2, width:width*2] = motionMaskEqualizedCLAHE
    totalImage[height:height*2, width*2:width*3] = totalHistogramImageAND
    totalImage[height:height*2, width*3:width*4] = totalHistogramImageOR
    totalImage[height:height*2, width*4:width*5] = totalHistogramImageXOR
    
    #Imagen ecualizada por histograma
    totalImage[height*2:height*3, :width] = equalizedHistogramImage
    totalImage[height*2:height*3, width:width*2] = motionMaskEqualizedHistogram
    totalImage[height*2:height*3, width*2:width*3] = totalCLAHEImageAND
    totalImage[height*2:height*3, width*3:width*4] = totalCLAHEImageOR
    totalImage[height*2:height*3, width*4:width*5] = totalCLAHEImageXOR
    
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


# |----------| | Iliminacion y Control de Ruido| |----------|
def equalizeHistogram (grayImage) -> np.ndarray:
    """Funcion para equalizar el histograma."""
    smoothedImgage = cv2.GaussianBlur(grayImage, (11, 11), 0)
    median_blurred = cv2.medianBlur(smoothedImgage, 5)
    equalized_image = cv2.equalizeHist(median_blurred)
    return equalized_image

def methodCLAHE (grayImage) -> np.ndarray:
    """Funcion para equalizar la imagen por el metodo CLAHE."""
    smoothedImgage = cv2.GaussianBlur(grayImage, (11, 11), 0)
    median_blurred = cv2.medianBlur(smoothedImgage, 5)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    equalized_image = clahe.apply(median_blurred)
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