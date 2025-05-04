import cv2, requests, numpy as np
from io import BytesIO
from flask import current_app
from config import Config as AppConfig

def video_capture_esp32():
    """Genera un stream MJPEG con ruido desde la cámara ESP32-CAM.

    Lee la configuración de `current_app.config` para construir la URL de
    streaming y procesa cada chunk añadiendo ruido aleatorio y devolviendo
    los frames en formato multipart JPEG.
    """
    #enviroments = current_app.config
    enviroments: AppConfig = current_app.config
    
    # IP Address
    _URL = enviroments.CAMERA_URL
    # Default Streaming Port
    _PORT = enviroments.CAMERA_PORT
    # Default streaming route
    _ST = enviroments.STREAMING_ST
    SEP = enviroments.STREAMING_SEP

    stream_url = ''.join([_URL,SEP,_PORT,_ST])
    res = requests.get(stream_url, stream=True)
    for chunk in res.iter_content(chunk_size=100000):

        if len(chunk) > 100:
            try:
                img_data = BytesIO(chunk)
                cv_img = cv2.imdecode(np.frombuffer(img_data.read(), np.uint8), 1)
                gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                N = 537
                height, width = gray.shape
                noise = np.full((height, width), 0, dtype=np.uint8)
                random_positions = (np.random.randint(0, height, N), np.random.randint(0, width, N))
                
                noise[random_positions[0], random_positions[1]] = 255

                noise_image = cv2.bitwise_or(gray, noise)

                total_image = np.zeros((height, width * 2), dtype=np.uint8)
                total_image[:, :width] = gray
                total_image[:, width:] = noise_image

                (flag, encodedImage) = cv2.imencode(".jpg", total_image)
                if not flag:
                    continue

                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

            except Exception as e:
                print(e)
                continue
    

def video_capture_local():
    """Genera un stream MJPEG en escala de grises desde la cámara local.

    Abre `cv2.VideoCapture(0)`, lee fotogramas, los convierte a gris
    y los emite codificados en JPEG para streaming HTTP.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara local")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, encoded = cv2.imencode('.jpg', gray)
            yield (b'--frame\r\n'                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
            
    finally:
        cap.release()


def select_capture():
    """Pregunta al usuario si usar cámara local o ESP32 y devuelve el generator."""
    print("Seleccione la fuente de video:")
    choice = input("¿Local (L) o ESP32 (E)? ").strip().lower()
    return video_capture_local() if choice=='l' else video_capture_esp32()
