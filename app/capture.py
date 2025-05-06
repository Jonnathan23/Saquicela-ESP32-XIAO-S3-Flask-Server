import cv2
import time

from app.utils.filters import filterImplementation_part_a
from app.data.backgroundSubtractor import background_subtractor_original
from app.data.backgroundSubtractor import background_subtractor_histogram
from app.data.backgroundSubtractor import background_subtractor_clahe


def video_capture_esp32():
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
    
    prev_time = time.perf_counter() 
    stream_url = ''.join([_URL,SEP,_PORT,_ST])
    
    cap = cv2.VideoCapture(stream_url)
    
    # Calentamiento del modelo de fondo
    if(not cap.isOpened()):
        raise RuntimeError(f"No se pudo abrir la cámara del EsP32-CAM en el URL: {stream_url}")
    for _ in range(30):
        ret, frame = cap.read()
        if not ret:
            break
        grayWarmup = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background_subtractor_original.apply(grayWarmup)
        background_subtractor_histogram.apply(grayWarmup)
        background_subtractor_clahe.apply(grayWarmup)
        
    # Captura de video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calcular FPS
        now = time.time()    
        fps = 1.0 / (now - prev_time) if now != prev_time else 0.0
        prev_time = now

        cv2.putText(grayImage,
                    f"FPS: {fps:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,            # escala de letra
                    255,          # color blanco en gris
                    2,            # grosor
                    cv2.LINE_AA)
    
       
        total_image = filterImplementation_part_a(grayImage)
        # Codifica el frame en JPEG
        
        flag, encoded = cv2.imencode('.jpg', total_image)
        if not flag:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encoded) +
                   b'\r\n')
        
        
    
    

def video_capture_local():
    """Genera un stream MJPEG en escala de grises desde la cámara local.

    Abre `cv2.VideoCapture(0)`, lee fotogramas, los convierte a gris
    y los emite codificados en JPEG para streaming HTTP.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara local")
    try:        
        prev_time = time.perf_counter()
        bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=1000,       # Cuántos frames recordar para construir el fondo
            varThreshold=25,    # Sensibilidad al cambio de píxel
            detectShadows=True  # Si quieres marcar sombras en gris oscuro
        )
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calcular FPS
            now = time.time()    
            fps = 1.0 / (now - prev_time) if now != prev_time else 0.0
            prev_time = now

            cv2.putText(grayImage,
                        f"FPS: {fps:.1f}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,            # escala de letra
                        255,          # color blanco en gris
                        2,            # grosor
                        cv2.LINE_AA)
            
            # Aplicar filtros
            totalImage = filterImplementation_part_a(grayImage)
            
            # Codifica el frame en JPEG
            _, encoded = cv2.imencode('.jpg', totalImage)
            yield (b'--frame\r\n'                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
            
    finally:
        cap.release()


def select_capture():
    """Pregunta al usuario si usar cámara local o ESP32 y devuelve el generator."""
    print("Seleccione la fuente de video:")
    choice = input("¿Local (L) o ESP32 (E)? ").strip().lower()
    return video_capture_local() if choice=='l' else video_capture_esp32()
