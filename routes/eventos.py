from flask.views import MethodView
from flask_smorest import Blueprint, abort

from extensions import db
from models import CatEvento
from schemas import EventoSchema

blp = Blueprint("eventos", __name__, url_prefix="/api/eventos",
                 description="Catálogo de tipos de evento (ENTRADA, SALIDA, etc.)")


@blp.route("")
class EventoList(MethodView):
    @blp.response(200, EventoSchema(many=True))
    def get(self):
        """Lista todos los eventos"""
        return CatEvento.query.all()

    @blp.arguments(EventoSchema)
    @blp.response(201, EventoSchema)
    def post(self, new_data):
        """Crea un nuevo tipo de evento"""
        evento = CatEvento(**new_data)
        db.session.add(evento)
        db.session.commit()
        return evento


@blp.route("/<int:id_evento>")
class EventoItem(MethodView):
    @blp.response(200, EventoSchema)
    def get(self, id_evento):
        """Obtiene un evento por id"""
        return CatEvento.query.get_or_404(id_evento, description="Evento no encontrado")

    @blp.arguments(EventoSchema)
    @blp.response(200, EventoSchema)
    def put(self, update_data, id_evento):
        """Actualiza un evento existente"""
        evento = CatEvento.query.get_or_404(id_evento, description="Evento no encontrado")
        for key, value in update_data.items():
            setattr(evento, key, value)
        db.session.commit()
        return evento

    @blp.response(204)
    def delete(self, id_evento):
        """Elimina un evento"""
        evento = CatEvento.query.get_or_404(id_evento, description="Evento no encontrado")
        db.session.delete(evento)
        db.session.commit()
