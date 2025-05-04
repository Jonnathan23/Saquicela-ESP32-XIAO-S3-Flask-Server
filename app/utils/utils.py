import cv2
import requests
import numpy as np
from io import BytesIO

def decode_jpeg_bytes(chunk: bytes) -> np.ndarray:
    """"Toma bytes JPEG y devielve un frame BGR"""
    buff = np.frombuffer(chunk, dtype=np.uint8)
    return cv2.imdecode(buff, cv2.IMREAD_COLOR)

