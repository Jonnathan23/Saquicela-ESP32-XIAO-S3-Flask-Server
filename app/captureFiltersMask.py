import cv2

from app.utils.filtersColor import filterImplementationPartB

def video_capture_esp32_filters_mask():
    """Genera un stream MJPEG con ruido desde la cámara ESP32-CAM.

    Lee la configuración de `current_app.config` para construir la URL de
    streaming y procesa cada chunk añadiendo ruido aleatorio y devolviendo
    los frames en formato multipart JPEG.
    """
    # IP Address
    _URL = 'http://192.168.2.13'
    # Default Streaming Port
    _PORT = '81'
    # Default streaming route
    _ST = '/stream'
    SEP = ':'    
   
    stream_url = ''.join([_URL,SEP,_PORT,_ST])
    
    cap = cv2.VideoCapture(stream_url)
    
    if(not cap.isOpened()):
        raise RuntimeError(f"No se pudo abrir la cámara del EsP32-CAM en el URL: {stream_url}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        total_image = filterImplementationPartB(frame)
        
        flag, encoded = cv2.imencode('.jpg', total_image)
        if not flag:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encoded) +
                   b'\r\n')
        
    
    

def video_capture_local_filters_mask():
    """Genera un stream MJPEG en escala de grises desde la cámara local.

    Abre `cv2.VideoCapture(0)`, lee fotogramas y los emite codificados en JPEG para streaming HTTP.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara local")
    try:                
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Aplicar filtros
            totalImage = filterImplementationPartB(frame)
            
            # Codifica el frame en JPEG
            _, encoded = cv2.imencode('.jpg', totalImage)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
            
    finally:
        cap.release()


def select_capture_filters_mask():
    """Pregunta al usuario si usar cámara local o ESP32 y devuelve el generator."""
    print("Seleccione la fuente de video:")
    choice = input("¿Local (L) o ESP32 (E)? ").strip().lower()
    return video_capture_local_filters_mask() if choice=='l' else video_capture_esp32_filters_mask()
