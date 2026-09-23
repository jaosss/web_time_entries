from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import func, case

from extensions import db
from models import RegistroAsistencia, CatEvento, Empleado, EmpresaVendor
from schemas import (
    AsistenciaSchema, AsistenciaQueryArgsSchema,
    ReporteDetalleSchema, ReporteDiarioSchema,
)

blp = Blueprint("asistencias", __name__, url_prefix="/api/asistencias",
                 description="Registros de asistencia (checadas) y reportes")


def _to_model_kwargs(data):
    kwargs = dict(data)
    lon = kwargs.pop("longitud", None)
    lat = kwargs.pop("latitud", None)
    kwargs["coordenadas_gps"] = (lon, lat) if lon is not None and lat is not None else None
    return kwargs


def _dump_extra(a):
    lon, lat = a.coordenadas_gps if a.coordenadas_gps else (None, None)
    a.longitud = lon
    a.latitud = lat
    return a


@blp.route("")
class AsistenciaList(MethodView):
    @blp.arguments(AsistenciaQueryArgsSchema, location="query")
    @blp.response(200, AsistenciaSchema(many=True))
    def get(self, args):
        """Lista registros de asistencia, con filtros opcionales"""
        query = RegistroAsistencia.query
        if "id_empleado" in args:
            query = query.filter(RegistroAsistencia.id_empleado == args["id_empleado"])
        if "fecha_desde" in args:
            query = query.filter(RegistroAsistencia.fecha_hora >= args["fecha_desde"])
        if "fecha_hasta" in args:
            query = query.filter(RegistroAsistencia.fecha_hora <= args["fecha_hasta"])
        query = query.order_by(RegistroAsistencia.fecha_hora.desc())
        return [_dump_extra(a) for a in query.all()]

    @blp.arguments(AsistenciaSchema)
    @blp.response(201, AsistenciaSchema)
    def post(self, new_data):
        """Registra una nueva checada"""
        a = RegistroAsistencia(**_to_model_kwargs(new_data))
        db.session.add(a)
        db.session.commit()
        return _dump_extra(a)


@blp.route("/<int:id_asistencia>")
class AsistenciaItem(MethodView):
    @blp.response(200, AsistenciaSchema)
    def get(self, id_asistencia):
        """Obtiene un registro de asistencia por id"""
        a = RegistroAsistencia.query.get_or_404(id_asistencia, description="Registro no encontrado")
        return _dump_extra(a)

    @blp.response(204)
    def delete(self, id_asistencia):
        """Elimina un registro de asistencia"""
        a = RegistroAsistencia.query.get_or_404(id_asistencia, description="Registro no encontrado")
        db.session.delete(a)
        db.session.commit()


@blp.route("/reporte-detalle")
class ReporteDetalle(MethodView):
    @blp.response(200, ReporteDetalleSchema(many=True))
    def get(self):
        """Equivalente al SELECT detallado del schema: cada checada con evento, empleado y empresa"""
        rows = (
            db.session.query(
                RegistroAsistencia.fecha_hora,
                CatEvento.nombre_evento,
                Empleado.nombre.label("empleado_nombre"),
                Empleado.tipo_personal,
                func.coalesce(EmpresaVendor.nombre_empresa, "NUESTRA EMPRESA (INTERNO)").label("empresa"),
            )
            .join(Empleado, RegistroAsistencia.id_empleado == Empleado.id_empleado)
            .join(CatEvento, RegistroAsistencia.id_evento == CatEvento.id_evento)
            .outerjoin(EmpresaVendor, Empleado.id_empresa_vendor == EmpresaVendor.id_empresa_vendor)
            .order_by(RegistroAsistencia.fecha_hora.desc())
            .all()
        )
        return [
            {
                "fecha_hora": r.fecha_hora,
                "nombre_evento": r.nombre_evento,
                "empleado_nombre": r.empleado_nombre,
                "tipo_personal": r.tipo_personal.value if r.tipo_personal else None,
                "empresa": r.empresa,
            }
            for r in rows
        ]


@blp.route("/reporte-diario")
class ReporteDiario(MethodView):
    @blp.response(200, ReporteDiarioSchema(many=True))
    def get(self):
        """Equivalente al SELECT de resumen diario: hora de entrada/salida por empleado y día"""
        dia = func.date(RegistroAsistencia.fecha_hora)
        rows = (
            db.session.query(
                dia.label("dia_laborado"),
                Empleado.codigo_empleado,
                (Empleado.nombre + " " + Empleado.apellido).label("empleado"),
                Empleado.tipo_personal,
                func.min(case((CatEvento.nombre_evento == "ENTRADA", RegistroAsistencia.fecha_hora))).label("hora_entrada"),
                func.max(case((CatEvento.nombre_evento == "SALIDA", RegistroAsistencia.fecha_hora))).label("hora_salida"),
            )
            .join(Empleado, RegistroAsistencia.id_empleado == Empleado.id_empleado)
            .join(CatEvento, RegistroAsistencia.id_evento == CatEvento.id_evento)
            .group_by(dia, Empleado.id_empleado, Empleado.codigo_empleado, Empleado.nombre,
                      Empleado.apellido, Empleado.tipo_personal)
            .order_by(dia.desc(), Empleado.nombre.asc())
            .all()
        )
        return [
            {
                "dia_laborado": str(r.dia_laborado) if r.dia_laborado else None,
                "codigo_empleado": r.codigo_empleado,
                "empleado": r.empleado,
                "tipo_personal": r.tipo_personal.value if r.tipo_personal else None,
                "hora_entrada": r.hora_entrada.strftime("%H:%M:%S") if r.hora_entrada else None,
                "hora_salida": r.hora_salida.strftime("%H:%M:%S") if r.hora_salida else None,
            }
            for r in rows
        ]
