import cv2
from flask import abort

from app.utils.filtersColor import implementFilterToImage

def _read_and_process_frame(source):
    """
    Abre un VideoCapture (0 para local o URL para ESP32),
    lee un solo frame, lo procesa y devuelve los bytes JPEG.
    """

    
    cap = cv2.VideoCapture(source)
    
    if(not cap.isOpened()):        
        abort(500, f"No se pudo abrir la fuente {source}")
    
    ret, frame = cap.read()
    cap.release()
    if not ret:
        abort(409, f"No se pudo leer el frame de la fuente {source}")        
    
    processedImage = implementFilterToImage(frame)
    
    flag, encoded = cv2.imencode('.jpg', processedImage)    
    if not flag:
        abort(500, "Error al codificar la imagen a JPEG")
        
    return encoded.tobytes()
        

def get_esp32_filtered_photo() -> bytes:
    # IP Address
    _URL = 'http://192.168.2.13'
    # Default Streaming Port
    _PORT = '81'
    # Default streaming route
    _ST = '/stream'
    SEP = ':'    
   
    stream_url = ''.join([_URL,SEP,_PORT,_ST])
    return _read_and_process_frame(stream_url)


def get_local_filtered_photo() -> bytes:
    return _read_and_process_frame(0)