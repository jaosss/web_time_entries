import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    load_dotenv()

    # Example: postgresql+psycopg2://user:password@localhost:5432/asistencia_db
    _DB_HOST = os.environ.get("DB_HOST", "")
    _DB_PORT = os.environ.get("DB_PORT", "5432")
    _DB_NAME = os.environ.get("DB_NAME", "")
    _DB_USER = os.environ.get("DB_USER", "")
    _DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"postgresql+psycopg://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}",
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
