from flask.views import MethodView
from flask_smorest import Blueprint

from extensions import db
from models import UbicacionAutorizada
from schemas import UbicacionSchema

blp = Blueprint("ubicaciones", __name__, url_prefix="/api/ubicaciones",
                 description="Ubicaciones autorizadas para marcar asistencia")


def _to_model_kwargs(data):
    """Pulls longitud/latitud out of the payload into the Point tuple the model expects."""
    kwargs = dict(data)
    lon = kwargs.pop("longitud")
    lat = kwargs.pop("latitud")
    kwargs["coordenadas"] = (lon, lat)
    return kwargs


def _dump_extra(u):
    """Splits the model's Point tuple back into longitud/latitud for the schema."""
    lon, lat = u.coordenadas if u.coordenadas else (None, None)
    u.longitud = lon
    u.latitud = lat
    return u


@blp.route("")
class UbicacionList(MethodView):
    @blp.response(200, UbicacionSchema(many=True))
    def get(self):
        """Lista todas las ubicaciones autorizadas"""
        return [_dump_extra(u) for u in UbicacionAutorizada.query.all()]

    @blp.arguments(UbicacionSchema)
    @blp.response(201, UbicacionSchema)
    def post(self, new_data):
        """Crea una nueva ubicación autorizada"""
        u = UbicacionAutorizada(**_to_model_kwargs(new_data))
        db.session.add(u)
        db.session.commit()
        return _dump_extra(u)


@blp.route("/<int:id_ubicacion>")
class UbicacionItem(MethodView):
    @blp.response(200, UbicacionSchema)
    def get(self, id_ubicacion):
        """Obtiene una ubicación por id"""
        u = UbicacionAutorizada.query.get_or_404(id_ubicacion, description="Ubicación no encontrada")
        return _dump_extra(u)

    @blp.arguments(UbicacionSchema)
    @blp.response(200, UbicacionSchema)
    def put(self, update_data, id_ubicacion):
        """Actualiza una ubicación existente"""
        u = UbicacionAutorizada.query.get_or_404(id_ubicacion, description="Ubicación no encontrada")
        kwargs = _to_model_kwargs(update_data)
        for key, value in kwargs.items():
            setattr(u, key, value)
        db.session.commit()
        return _dump_extra(u)

    @blp.response(204)
    def delete(self, id_ubicacion):
        """Elimina una ubicación"""
        u = UbicacionAutorizada.query.get_or_404(id_ubicacion, description="Ubicación no encontrada")
        db.session.delete(u)
        db.session.commit()
