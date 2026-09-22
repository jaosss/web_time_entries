from flask import Blueprint, render_template

# Creamos un blueprint normal para el sitio web
web_blp = Blueprint('web', __name__)

@web_blp.route('/')
def home():
    """Ruta para la página de inicio del sitio web."""
    return render_template('index.html')

@web_blp.route('/dashboard')
def dashboard():
    """Ruta para ver reportes gráficos de asistencia en la web."""
    # Aquí puedes consultar la BD y pasar los datos a la plantilla
    return render_template('reportes.html')
