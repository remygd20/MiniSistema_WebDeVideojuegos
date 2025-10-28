from flask import Blueprint

# Creamos el Blueprint para la API
# 'api' será el nombre para los url_for (ej. 'api.get_juegos')
api_bp = Blueprint('api', __name__)

# Importamos las rutas (routes.py) al final
# para evitar importaciones circulares
from . import routes