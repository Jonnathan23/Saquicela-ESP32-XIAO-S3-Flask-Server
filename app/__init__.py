from flask import Flask
from config import Config as AppConfig
from .routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    # Registrar blueprint de rutas
    app.register_blueprint(main_bp)
    return app