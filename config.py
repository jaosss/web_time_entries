import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Example: postgresql+psycopg2://user:password@localhost:5432/asistencia_db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/asistencia_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # --- flask-smorest / OpenAPI settings ---
    API_TITLE = "API de Control de Asistencias"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
