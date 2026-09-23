from flask.views import MethodView
from flask_smorest import Blueprint

from extensions import db
from models import EmpresaVendor
from schemas import EmpresaVendorSchema

blp = Blueprint("empresas-vendors", __name__, url_prefix="/api/empresas-vendors",
                 description="Empresas externas (vendors) cuyo personal marca asistencia")


@blp.route("")
class VendorList(MethodView):
    @blp.response(200, EmpresaVendorSchema(many=True))
    def get(self):
        """Lista todas las empresas vendor"""
        return EmpresaVendor.query.all()

    @blp.arguments(EmpresaVendorSchema)
    @blp.response(201, EmpresaVendorSchema)
    def post(self, new_data):
        """Crea una nueva empresa vendor"""
        v = EmpresaVendor(**new_data)
        db.session.add(v)
        db.session.commit()
        return v


@blp.route("/<int:id_empresa_vendor>")
class VendorItem(MethodView):
    @blp.response(200, EmpresaVendorSchema)
    def get(self, id_empresa_vendor):
        """Obtiene una empresa vendor por id"""
        return EmpresaVendor.query.get_or_404(id_empresa_vendor, description="Empresa no encontrada")

    @blp.arguments(EmpresaVendorSchema)
    @blp.response(200, EmpresaVendorSchema)
    def put(self, update_data, id_empresa_vendor):
        """Actualiza una empresa vendor"""
        v = EmpresaVendor.query.get_or_404(id_empresa_vendor, description="Empresa no encontrada")
        for key, value in update_data.items():
            setattr(v, key, value)
        db.session.commit()
        return v

    @blp.response(204)
    def delete(self, id_empresa_vendor):
        """Elimina una empresa vendor"""
        v = EmpresaVendor.query.get_or_404(id_empresa_vendor, description="Empresa no encontrada")
        db.session.delete(v)
        db.session.commit()
