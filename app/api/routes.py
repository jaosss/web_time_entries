# app/api/routes.py
from flask_smorest import Blueprint  # <- DEBE SER ESTE, NO EL DE FLASK
from flask.views import MethodView

# Asegúrate de que se llame 'blp' tal como lo importas en __init__.py
blp = Blueprint("Asistencias", __name__, description="Operaciones de la API")

@blp.route("/asistencias")
class Asistencias(MethodView):
    def post(self):
        return {"mensaje": "test"}
