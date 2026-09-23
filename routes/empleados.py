from flask.views import MethodView
from flask_smorest import Blueprint

from extensions import db
from models import Empleado
from schemas import EmpleadoSchema, EmpleadoQueryArgsSchema

blp = Blueprint("empleados", __name__, url_prefix="/api/empleados",
                 description="Empleados internos y de empresas vendor")


@blp.route("")
class EmpleadoList(MethodView):
    @blp.arguments(EmpleadoQueryArgsSchema, location="query")
    @blp.response(200, EmpleadoSchema(many=True))
    def get(self, args):
        """Lista empleados, con filtros opcionales (tipo_personal, activo)"""
        query = Empleado.query
        if "tipo_personal" in args:
            query = query.filter(Empleado.tipo_personal == args["tipo_personal"])
        if "activo" in args:
            query = query.filter(Empleado.activo == args["activo"])
        return query.all()

    @blp.arguments(EmpleadoSchema)
    @blp.response(201, EmpleadoSchema)
    def post(self, new_data):
        """Crea un nuevo empleado"""
        e = Empleado(**new_data)
        db.session.add(e)
        db.session.commit()
        return e


@blp.route("/<int:id_empleado>")
class EmpleadoItem(MethodView):
    @blp.response(200, EmpleadoSchema)
    def get(self, id_empleado):
        """Obtiene un empleado por id"""
        return Empleado.query.get_or_404(id_empleado, description="Empleado no encontrado")

    @blp.arguments(EmpleadoSchema)
    @blp.response(200, EmpleadoSchema)
    def put(self, update_data, id_empleado):
        """Actualiza un empleado existente"""
        e = Empleado.query.get_or_404(id_empleado, description="Empleado no encontrado")
        for key, value in update_data.items():
            setattr(e, key, value)
        db.session.commit()
        return e

    @blp.response(204)
    def delete(self, id_empleado):
        """Elimina un empleado (cascada sobre sus asistencias)"""
        e = Empleado.query.get_or_404(id_empleado, description="Empleado no encontrado")
        db.session.delete(e)
        db.session.commit()
