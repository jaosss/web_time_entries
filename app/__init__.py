# app/__init__.py
from flask import Flask
from flask_smorest import Api
from app.api.routes import blp as ApiBlueprint

def create_app():
    app = Flask(__name__)
    
    # Configuraciones requeridas por flask-smorest
    app.config["API_TITLE"] = "Control Asistencias API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/api"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cloudflare.com"
    
    # 1. Inicializar la extensión API pasándole la app
    api = Api(app)
    
    # 2. Registrar el blueprint usando el objeto 'api', NO 'app.register_blueprint'
    api.register_blueprint(ApiBlueprint)
    
    return app
