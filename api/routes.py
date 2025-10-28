from flask import jsonify, request, abort
from . import api_bp
from models import db, Juego

# --- Documentación y Ruta 1: GET /api/juegos (Obtener TODOS) ---
@api_bp.route('/juegos', methods=['GET'])
def get_juegos():
    """
    Endpoint: GET /api/juegos
    Descripción: Devuelve una lista de todos los juegos.
    """
    juegos = Juego.query.all()
    # Convertimos cada objeto 'juego' a su formato de diccionario
    juegos_list = [juego.to_dict() for juego in juegos]
    return jsonify(juegos_list), 200 # 200 OK

# --- Documentación y Ruta 2: GET /api/juegos/<id> (Obtener UNO) ---
@api_bp.route('/juegos/<int:id>', methods=['GET'])
def get_juego(id):
    """
    Endpoint: GET /api/juegos/<id>
    Descripción: Devuelve un solo juego por su ID.
    """
    # get_or_404 es una maravilla: si no lo encuentra, automáticamente
    # devuelve un error 404 Not Found.
    juego = Juego.query.get_or_404(id)
    return jsonify(juego.to_dict()), 200 # 200 OK

# --- Documentación y Ruta 3: POST /api/juegos (Crear UNO) ---
@api_bp.route('/juegos', methods=['POST'])
def create_juego():
    """
    Endpoint: POST /api/juegos
    Descripción: Crea un nuevo juego.
    Datos esperados (JSON):
    {
        "nombre": "Nombre del juego",
        "descripcion": "Descripción...",
        "precio": 19.99
    }
    """
    data = request.get_json()

    # Validación de entrada
    if not data or 'nombre' not in data or 'precio' not in data:
        # abort(400) es la forma correcta de devolver un 400 Bad Request
        abort(400, description="Faltan datos (nombre, precio) en el JSON.")

    # Creamos el nuevo objeto Juego
    nuevo_juego = Juego(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ""), # .get es más seguro
        precio=data['precio']
    )
    
    db.session.add(nuevo_juego)
    db.session.commit()
    
    # Devolvemos el objeto recién creado y el código 201 Created
    return jsonify(nuevo_juego.to_dict()), 201

# --- Documentación y Ruta 4: PUT /api/juegos/<id> (Actualizar UNO) ---
@api_bp.route('/juegos/<int:id>', methods=['PUT'])
def update_juego(id):
    """
    Endpoint: PUT /api/juegos/<id>
    Descripción: Actualiza un juego existente por su ID.
    Datos esperados (JSON):
    {
        "nombre": "Nuevo nombre",
        "descripcion": "Nueva descripción",
        "precio": 29.99
    }
    """
    juego = Juego.query.get_or_404(id)
    data = request.get_json()

    if not data:
        abort(400, description="No se enviaron datos en el JSON.")

    # Actualizamos los campos. Usamos .get() para permitir
    # actualizaciones parciales (ej. solo cambiar el precio)
    juego.nombre = data.get('nombre', juego.nombre)
    juego.descripcion = data.get('descripcion', juego.descripcion)
    juego.precio = data.get('precio', juego.precio)

    db.session.commit()
    
    return jsonify(juego.to_dict()), 200 # 200 OK

# --- Documentación y Ruta 5: DELETE /api/juegos/<id> (Eliminar UNO) ---
@api_bp.route('/juegos/<int:id>', methods=['DELETE'])
def delete_juego(id):
    """
    Endpoint: DELETE /api/juegos/<id>
    Descripción: Elimina un juego existente por su ID.
    """
    juego = Juego.query.get_or_404(id)
    
    db.session.delete(juego)
    db.session.commit()
    
    # Un DELETE exitoso debe devolver un código 204 No Content
    # y este código NO DEBE tener cuerpo en la respuesta.
    return '', 204

# --- Manejador de Errores (Bonus) ---
# Esto captura los errores 404 (Not Found) y 400 (Bad Request)
# y los devuelve en formato JSON, que es lo correcto para una API.
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'No encontrado', 'mensaje': str(error)}), 404

@api_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Solicitud incorrecta', 'mensaje': str(error)}), 400