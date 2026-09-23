from marshmallow import Schema, fields, validate

from models import TipoPersonalEnum


class EventoSchema(Schema):
    id_evento = fields.Int(dump_only=True)
    nombre_evento = fields.Str(required=True, metadata={"example": "ENTRADA"})


class UbicacionSchema(Schema):
    id_ubicacion = fields.Int(dump_only=True)
    nombre_ubicacion = fields.Str(required=True, metadata={"example": "Oficina Central"})
    longitud = fields.Float(required=True, metadata={"description": "Longitud (X del POINT)"})
    latitud = fields.Float(required=True, metadata={"description": "Latitud (Y del POINT)"})
    radio_tolerancia_metros = fields.Int(load_default=50, dump_default=50)
    activo = fields.Bool(load_default=True, dump_default=True)


class EmpresaVendorSchema(Schema):
    id_empresa_vendor = fields.Int(dump_only=True)
    nombre_empresa = fields.Str(required=True)
    rfc_o_tax_id = fields.Str(allow_none=True)
    contacto_nombre = fields.Str(allow_none=True)
    contacto_telefono = fields.Str(allow_none=True)
    activo = fields.Bool(load_default=True, dump_default=True)
    creado_en = fields.DateTime(dump_only=True)


class EmpleadoSchema(Schema):
    id_empleado = fields.Int(dump_only=True)
    codigo_empleado = fields.Str(required=True)
    tipo_personal = fields.Str(
        load_default=TipoPersonalEnum.INTERNO.value,
        dump_default=TipoPersonalEnum.INTERNO.value,
        validate=validate.OneOf([e.value for e in TipoPersonalEnum]),
    )
    id_empresa_vendor = fields.Int(allow_none=True, metadata={"description": "Requerido si tipo_personal es VENDOR"})
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    puesto = fields.Str(allow_none=True)
    id_ubicacion_asignada = fields.Int(allow_none=True)
    activo = fields.Bool(load_default=True, dump_default=True)
    creado_en = fields.DateTime(dump_only=True)


class EmpleadoQueryArgsSchema(Schema):
    tipo_personal = fields.Str(validate=validate.OneOf([e.value for e in TipoPersonalEnum]))
    activo = fields.Bool()


class AsistenciaSchema(Schema):
    id_asistencia = fields.Int(dump_only=True)
    id_empleado = fields.Int(required=True)
    id_evento = fields.Int(required=True)
    fecha_hora = fields.DateTime(required=True, metadata={"example": "2026-09-22T08:00:00-06:00"})
    id_ubicacion_marcada = fields.Int(allow_none=True)
    longitud = fields.Float(allow_none=True, metadata={"description": "Longitud GPS al momento de checar"})
    latitud = fields.Float(allow_none=True, metadata={"description": "Latitud GPS al momento de checar"})
    dispositivo_origen = fields.Str(allow_none=True)
    creado_en = fields.DateTime(dump_only=True)


class AsistenciaQueryArgsSchema(Schema):
    id_empleado = fields.Int()
    fecha_desde = fields.Date()
    fecha_hasta = fields.Date()


class ReporteDetalleSchema(Schema):
    fecha_hora = fields.DateTime()
    nombre_evento = fields.Str()
    empleado_nombre = fields.Str()
    tipo_personal = fields.Str()
    empresa = fields.Str()


class ReporteDiarioSchema(Schema):
    dia_laborado = fields.Str()
    codigo_empleado = fields.Str()
    empleado = fields.Str()
    tipo_personal = fields.Str()
    hora_entrada = fields.Str(allow_none=True)
    hora_salida = fields.Str(allow_none=True)
