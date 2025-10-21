from flask import Blueprint

# Creamos el blueprint
auth_bp = Blueprint('auth', __name__)

# Importamos las vistas (views.py) al final 
from . import views