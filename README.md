# API de Control de Asistencias — Flask + SQLAlchemy + flask-smorest

Misma API que la versión con Flask-RESTX, reescrita sobre **flask-smorest**:
Blueprints basados en `MethodView` + Schemas de **marshmallow** para
validación y serialización, con Swagger UI generado automáticamente
(OpenAPI 3) a partir de esos mismos schemas.

Los modelos (`models.py`), la conexión a la base de datos y
`schema_fixed.sql` son idénticos a la versión anterior — lo único que
cambia es la capa de framework/validación/documentación.

## 1. Instalación

```bash
cd flask_smorest_asistencia_api
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Base de datos

```bash
createdb asistencia_db
psql -d asistencia_db -f schema_fixed.sql
cp .env.example .env
# Ajusta DATABASE_URL en .env
```

## 3. Ejecutar

Con Python directo:
```bash
python app.py
```

O con el comando `flask`:
```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000
```

- API: `http://localhost:5000/api/...`
- **Swagger UI**: `http://localhost:5000/swagger`
- OpenAPI JSON crudo: `http://localhost:5000/openapi.json`
- Health check: `http://localhost:5000/health`

## 4. Qué cambió respecto a la versión con Flask-RESTX

| Concepto | Flask-RESTX | flask-smorest |
|---|---|---|
| Agrupar rutas | `Namespace` | `Blueprint` (de `flask_smorest`, no el de Flask puro) |
| Definir un recurso | clase `Resource` | clase `MethodView` |
| Definir el "shape" de los datos | `ns.model()` (diccionario de `fields`) | `Schema` de marshmallow (`schemas/__init__.py`) |
| Validar el body del request | `@ns.expect(model, validate=True)` | `@blp.arguments(Schema)` — inyecta los datos ya validados como argumento |
| Serializar la respuesta | `@ns.marshal_with(model)` | `@blp.response(status_code, Schema)` |
| Validar query params | `request.args` manual | `@blp.arguments(Schema, location="query")` — ver `EmpleadoQueryArgsSchema` y `AsistenciaQueryArgsSchema` |
| 404 automático | `Model.query.get_or_404(id)` | igual, `Model.query.get_or_404(id, description=...)` |
| Doc de Swagger | se arma en `Api(app, title=..., doc="/swagger")` | se arma con `API_TITLE`/`API_VERSION`/`OPENAPI_*` en `config.py` |

La estructura de carpetas es análoga:

```
flask_smorest_asistencia_api/
├── app.py                   # App factory, registra blueprints
├── config.py                  # Incluye ajustes OpenAPI (API_TITLE, etc.)
├── extensions.py               # SQLAlchemy compartido
├── models.py                   # (sin cambios) modelos SQLAlchemy
├── schemas/__init__.py          # Schemas de marshmallow (reemplazan ns.model)
├── requirements.txt
├── schema_fixed.sql
└── routes/
    ├── eventos.py                # /api/eventos
    ├── ubicaciones.py             # /api/ubicaciones
    ├── vendors.py                 # /api/empresas-vendors
    ├── empleados.py                # /api/empleados (con filtros por query)
    └── asistencias.py              # /api/asistencias + reportes
```

## 5. Notas de diseño

- **Coordenadas (`POINT`)**: igual que antes, el modelo guarda una tupla
  `(longitud, latitud)`. Como marshmallow no puede volcar directamente un
  atributo `coordenadas` (tupla) en dos campos separados del schema
  (`longitud`/`latitud`), las rutas de `ubicaciones.py` y `asistencias.py`
  usan un helper `_dump_extra()` que copia esos valores como atributos
  sueltos en el objeto antes de serializarlo, y `_to_model_kwargs()` para
  reconstruir la tupla al guardar.
- **Filtros por query string**: en flask-smorest se validan igual que el
  body, con un `Schema` aparte y `location="query"` — ve
  `EmpleadoQueryArgsSchema` (`tipo_personal`, `activo`) y
  `AsistenciaQueryArgsSchema` (`id_empleado`, `fecha_desde`, `fecha_hasta`).
- **Reportes**: `/api/asistencias/reporte-detalle` y
  `/api/asistencias/reporte-diario` siguen replicando los dos `SELECT` que
  traía `schema.sql`.
