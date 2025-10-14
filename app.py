# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Juego  # <-- CAMBIO IMPORTANTE
import controlador_juegos

app = Flask(__name__)

# Configuración de la Base de Datos (esto no cambia)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola1234*@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Aquí conectamos el objeto db (importado de models) con nuestra app
db.init_app(app) # <-- CAMBIO IMPORTANTE

# --- RUTAS (No cambian) ---
@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

# (El resto de tus rutas @app.route se quedan exactamente igual)
@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    return redirect(url_for('juegos'))

@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(id, nombre, descripcion, precio)
    return redirect(url_for('juegos'))

@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    id = request.form["id"]
    controlador_juegos.eliminar_juego(id)
    return redirect(url_for('juegos'))


# --- BLOQUE DE EJECUCIÓN ---
if __name__ == '__main__':
    # Esto crea las tablas si no existen, conectándose a tu BD vieja sin borrar nada
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)