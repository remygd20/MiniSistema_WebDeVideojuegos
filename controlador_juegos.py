from models import db, Juego

# Inserta un nuevo juego en la base de datos
def insertar_juego(nombre, descripcion, precio):
    nuevo_juego = Juego(nombre=nombre, descripcion=descripcion, precio=precio)
    db.session.add(nuevo_juego)
    db.session.commit()

# Devuelve una lista con todos los juegos
def obtener_juegos():
    return Juego.query.all()

# Elimina un juego por su ID
def eliminar_juego(id):
    juego = Juego.query.get(id)
    if juego:
        db.session.delete(juego)
        db.session.commit()

# Devuelve un solo juego buscado por su ID
def obtener_juego_por_id(id):
    return Juego.query.get(id)

# Actualiza los datos de un juego existente
def actualizar_juego(id, nombre, descripcion, precio):
    juego = Juego.query.get(id)
    if juego:
        juego.nombre = nombre
        juego.descripcion = descripcion
        juego.precio = precio
        db.session.commit()