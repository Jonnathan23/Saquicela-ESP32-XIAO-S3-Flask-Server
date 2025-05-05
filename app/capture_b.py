import cv2, requests, numpy as np
from io import BytesIO
import time

from app.utils.filters import filterImplementationPartB

def video_capture_esp32_part_b():
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
    res = requests.get(stream_url, stream=True)
    for chunk in res.iter_content(chunk_size=100000):

        if len(chunk) > 100:
            try:
                img_data = BytesIO(chunk)
                cv_img = cv2.imdecode(np.frombuffer(img_data.read(), np.uint8), 1)                
                image = cv2.cvtColor(cv_img, cv2.COLOR_BAYER_BG2RGB)
                
                # Calcular FPS
                now = time.time()    
                fps = 1.0 / (now - prev_time) if now != prev_time else 0.0
                prev_time = now

                cv2.putText(image,
                            f"FPS: {fps:.1f}",
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,            # escala de letra
                            255,          # color blanco en gris
                            2,            # grosor
                            cv2.LINE_AA)
    
               
                total_image = filterImplementationPartB(cv_img)
                # Codifica el frame en JPEG
                (flag, encodedImage) = cv2.imencode(".jpg", total_image)
                if not flag:
                    continue

                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

            except Exception as e:
                print(e)
                continue
    

def video_capture_local_part_b():
    """Genera un stream MJPEG en escala de grises desde la cámara local.

    Abre `cv2.VideoCapture(0)`, lee fotogramas y los emite codificados en JPEG para streaming HTTP.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara local")
    try:        
        prev_time = time.perf_counter()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2RGB)
            
            # Calcular FPS
            now = time.time()    
            fps = 1.0 / (now - prev_time) if now != prev_time else 0.0
            prev_time = now

            cv2.putText(image,
                        f"FPS: {fps:.1f}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,            # escala de letra
                        255,          # color blanco en gris
                        2,            # grosor
                        cv2.LINE_AA)
            
            # Aplicar filtros
            totalImage = filterImplementationPartB(image)
            
            # Codifica el frame en JPEG
            _, encoded = cv2.imencode('.jpg', totalImage)
            yield (b'--frame\r\n'                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
            
    finally:
        cap.release()


def select_capture_part_b():
    """Pregunta al usuario si usar cámara local o ESP32 y devuelve el generator."""
    print("Seleccione la fuente de video:")
    choice = input("¿Local (L) o ESP32 (E)? ").strip().lower()
    return video_capture_local_part_b() if choice=='l' else video_capture_esp32_part_b()
