# web_time_entries

web_time_entries/
│
├── app/                        # Paquete principal de la aplicación
│   ├── __init__.py             # Inicializa la App Factory de Flask
│   ├── config.py               # Configuración de entornos (Dev, Prod, BD)
│   ├── db.py                   # Conexión/Inicialización de la base de datos
│   │
│   ├── api/                    # MÓDULO 1: REST API (flask-smorest)
│   │   ├── __init__.py         # Define el Blueprint de la API
│   │   ├── routes.py           # Endpoints de la API (asistencias, empleados)
│   │   └── schemas.py          # Esquemas de validación (Marshmallow)
│   │
│   ├── web/                    # MÓDULO 2: SITIO WEB (Frontend)
│   │   ├── __init__.py         # Define el Blueprint del sitio web
│   │   └── routes.py           # Rutas que renderizan páginas HTML
│   │
│   ├── static/                 # Archivos estáticos del Sitio Web
│   │   ├── css/                # Hojas de estilo (styles.css)
│   │   ├── js/                 # Scripts de JavaScript
│   │   └── images/             # Logos e imágenes del sitio
│   │
│   └── templates/              # Plantillas HTML (Jinja2)
│       ├── base.html           # Diseño/Estructura global de la web
│       ├── index.html          # Página de inicio
│       └── reportes.html       # Página web para ver las asistencias
│
├── run.py                      # Punto de entrada para arrancar el servidor
├── requirements.txt            # Dependencias del proyecto
└── .env                        # Variables de entorno secretas (Credenciales BD)
