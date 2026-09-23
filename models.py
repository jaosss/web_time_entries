import enum
import re

from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, ForeignKey,
    DateTime, UniqueConstraint, Enum as SAEnum
)
from sqlalchemy.types import UserDefinedType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from extensions import db


# ------------------------------------------------------------------
# Custom type to map PostgreSQL's native POINT type to a Python tuple
# (longitud, latitud), matching the convention used in schema.sql.
# ------------------------------------------------------------------
class Point(UserDefinedType):
    cache_ok = True

    def get_col_spec(self):
        return "POINT"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            lon, lat = value
            return f"({lon},{lat})"
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            match = re.match(r"\(([^,]+),([^,]+)\)", str(value))
            if match:
                return (float(match.group(1)), float(match.group(2)))
            return value
        return process


class TipoPersonalEnum(str, enum.Enum):
    INTERNO = "INTERNO"
    VENDOR = "VENDOR"


class CatEvento(db.Model):
    __tablename__ = "cat_eventos"

    id_evento = Column(Integer, primary_key=True)
    nombre_evento = Column(String(50), nullable=False, unique=True)

    def to_dict(self):
        return {"id_evento": self.id_evento, "nombre_evento": self.nombre_evento}


class UbicacionAutorizada(db.Model):
    __tablename__ = "ubicaciones_autorizadas"

    id_ubicacion = Column(Integer, primary_key=True)
    nombre_ubicacion = Column(String(100), nullable=False)
    coordenadas = Column(Point, nullable=False)
    radio_tolerancia_metros = Column(Integer, nullable=False, default=50)
    activo = Column(Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id_ubicacion": self.id_ubicacion,
            "nombre_ubicacion": self.nombre_ubicacion,
            "coordenadas": self.coordenadas,
            "radio_tolerancia_metros": self.radio_tolerancia_metros,
            "activo": self.activo,
        }


class EmpresaVendor(db.Model):
    __tablename__ = "empresas_vendors"

    id_empresa_vendor = Column(Integer, primary_key=True)
    nombre_empresa = Column(String(100), nullable=False, unique=True)
    rfc_o_tax_id = Column(String(20))
    contacto_nombre = Column(String(100))
    contacto_telefono = Column(String(20))
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    empleados = relationship("Empleado", back_populates="empresa_vendor")

    def to_dict(self):
        return {
            "id_empresa_vendor": self.id_empresa_vendor,
            "nombre_empresa": self.nombre_empresa,
            "rfc_o_tax_id": self.rfc_o_tax_id,
            "contacto_nombre": self.contacto_nombre,
            "contacto_telefono": self.contacto_telefono,
            "activo": self.activo,
            "creado_en": self.creado_en.isoformat() if self.creado_en else None,
        }


class Empleado(db.Model):
    __tablename__ = "empleados"

    id_empleado = Column(Integer, primary_key=True)
    codigo_empleado = Column(String(50), nullable=False, unique=True)
    tipo_personal = Column(
        SAEnum(TipoPersonalEnum, name="tipo_personal_enum", create_type=False),
        nullable=False,
        default=TipoPersonalEnum.INTERNO,
    )
    id_empresa_vendor = Column(
        Integer, ForeignKey("empresas_vendors.id_empresa_vendor", ondelete="SET NULL")
    )
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    puesto = Column(String(100))
    id_ubicacion_asignada = Column(Integer, ForeignKey("ubicaciones_autorizadas.id_ubicacion"))
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    empresa_vendor = relationship("EmpresaVendor", back_populates="empleados")
    ubicacion_asignada = relationship("UbicacionAutorizada")
    asistencias = relationship("RegistroAsistencia", back_populates="empleado", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_empleado": self.id_empleado,
            "codigo_empleado": self.codigo_empleado,
            "tipo_personal": self.tipo_personal.value if self.tipo_personal else None,
            "id_empresa_vendor": self.id_empresa_vendor,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "puesto": self.puesto,
            "id_ubicacion_asignada": self.id_ubicacion_asignada,
            "activo": self.activo,
            "creado_en": self.creado_en.isoformat() if self.creado_en else None,
        }


class RegistroAsistencia(db.Model):
    __tablename__ = "registro_asistencias"
    __table_args__ = (
        UniqueConstraint("id_empleado", "id_evento", "fecha_hora", name="uq_empleado_evento_hora"),
    )

    id_asistencia = Column(BigInteger, primary_key=True)
    id_empleado = Column(Integer, ForeignKey("empleados.id_empleado", ondelete="CASCADE"), nullable=False)
    id_evento = Column(Integer, ForeignKey("cat_eventos.id_evento"), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), nullable=False)
    id_ubicacion_marcada = Column(Integer, ForeignKey("ubicaciones_autorizadas.id_ubicacion"))
    coordenadas_gps = Column(Point)
    dispositivo_origen = Column(String(100))
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    empleado = relationship("Empleado", back_populates="asistencias")
    evento = relationship("CatEvento")
    ubicacion_marcada = relationship("UbicacionAutorizada")

    def to_dict(self):
        return {
            "id_asistencia": self.id_asistencia,
            "id_empleado": self.id_empleado,
            "id_evento": self.id_evento,
            "fecha_hora": self.fecha_hora.isoformat() if self.fecha_hora else None,
            "id_ubicacion_marcada": self.id_ubicacion_marcada,
            "coordenadas_gps": self.coordenadas_gps,
            "dispositivo_origen": self.dispositivo_origen,
            "creado_en": self.creado_en.isoformat() if self.creado_en else None,
        }
