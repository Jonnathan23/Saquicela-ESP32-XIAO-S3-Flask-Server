from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    CAMERA_URL    = os.getenv("CAMERA_URL")
    CAMERA_PORT   = os.getenv("CAMERA_PORT")
    STREAMING_ST  = os.getenv("STREAMING_ST")
    STREAMING_SEP = os.getenv("STREAMING_SEP", ":")