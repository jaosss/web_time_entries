from flask import Flask
from flask_smorest import Api

from config import Config
from extensions import db

from routes.eventos import blp as eventos_blp
from routes.ubicaciones import blp as ubicaciones_blp
from routes.vendors import blp as vendors_blp
from routes.empleados import blp as empleados_blp
from routes.asistencias import blp as asistencias_blp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    api = Api(app)

    api.register_blueprint(eventos_blp)
    api.register_blueprint(ubicaciones_blp)
    api.register_blueprint(vendors_blp)
    api.register_blueprint(empleados_blp)
    api.register_blueprint(asistencias_blp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
