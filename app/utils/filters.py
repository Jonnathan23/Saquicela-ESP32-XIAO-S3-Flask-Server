import cv2
import numpy as np

import app.data.data as data
from app.bitwiseOperations import selectedOperation
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
    
    '''TODO:
    # Imagen ecualizada
    equalizedHistogramImage = equalizeHistogram(grayImage)
    equalizedCLAHEImage = methodCLAHE(grayImage)
    
    # Extraer el fondo    
    motionMask = subtractBackground(grayImage,data.background_subtractor_original)         
    motionMaskEqualizedHistogram = subtractBackground(equalizedHistogramImage,data.background_subtractor_histogram)    
    motionMaskEqualizedCLAHE = subtractBackground(equalizedCLAHEImage,data.background_subtractor_clahe)     


    # Resultado de bitwise_operations Con la operacion seleccionada

    totalOriginalImage = selectedOperation[data.operationMask](grayImage, motionMask)
    totalHistogramImage = selectedOperation[data.operationMask](equalizedHistogramImage, motionMask)
    totalCLAHEImage = selectedOperation[data.operationMask](equalizedCLAHEImage, motionMask)
    
    #todo: --------------'''
    normalImage, mask, equalizedImage = implementEqualize(grayImage)
    

    #* Crear imagen total -> gris + mascara + bitwise_operations
    totalImage = np.full((height, width*3), 0, dtype=np.uint8)    
    totalImage = np.zeros((height, width *3), dtype=np.uint8)
    
    #Imagen original
    totalImage[:height, :width] = normalImage
    totalImage[:height, width:width*2] = mask
    totalImage[:height, width*2:width*3] = equalizedImage   
        
    '''
    #Imagen ecualizada por CLAHE
    totalImage[height:height*2, :width] = equalizedCLAHEImage
    totalImage[height:height*2, width:width*2] = motionMaskEqualizedCLAHE
    totalImage[height:height*2, width*2:width*3] = totalHistogramImage    
    
    #Imagen ecualizada por histograma
    totalImage[height*2:height*3, :width] = equalizedHistogramImage
    totalImage[height*2:height*3, width:width*2] = motionMaskEqualizedHistogram
    totalImage[height*2:height*3, width*2:width*3] = totalCLAHEImage
    
    '''
    
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

def implementEqualize(grayImage:np.ndarray):
    '''Implementa el tipo de filtro seleccionado'''
    if(data.equalizeOption == data.EqualizeSelectOptions.original):
        motionMask = subtractBackground(grayImage,data.background_subtractor_original)
        totalOriginalImage = selectedOperation[data.operationMask](grayImage, motionMask)
        return grayImage,motionMask,totalOriginalImage
    
    if(data.equalizeOption == data.EqualizeSelectOptions.histogram):
        equalizedHistogramImage = equalizeHistogram(grayImage)
        motionMaskEqualizedHistogram = subtractBackground(equalizedHistogramImage,data.background_subtractor_histogram)
        totalHistogramImage = selectedOperation[data.operationMask](equalizedHistogramImage, motionMaskEqualizedHistogram)
        return equalizedHistogramImage, motionMaskEqualizedHistogram, totalHistogramImage
    
    if(data.equalizeOption == data.EqualizeSelectOptions.clahe):
        equalizedCLAHEImage = methodCLAHE(grayImage)
        motionMaskEqualizedCLAHE = subtractBackground(equalizedCLAHEImage,data.background_subtractor_clahe)   
        totalCLAHEImage = selectedOperation[data.operationMask](equalizedCLAHEImage, motionMaskEqualizedCLAHE)
        return equalizedCLAHEImage, motionMaskEqualizedCLAHE, totalCLAHEImage
        

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