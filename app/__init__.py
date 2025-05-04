from flask import Flask
from .routes import main_bp

def create_app():
    app = Flask(__name__)    

    # Registrar blueprint de rutas
    app.register_blueprint(main_bp)
    return app