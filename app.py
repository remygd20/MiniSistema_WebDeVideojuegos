from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Juego, User
import controlador_juegos
from auth import auth_bp
from flask_login import LoginManager, login_required, current_user

app = Flask(__name__)

# Configuración de la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola1234*@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mi-clave-secreta-muy-segura-12345'

# Se inicializa la base de datos con la configuración de la app
db.init_app(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Apunta a la vista del blueprint
login_manager.login_view = 'auth.login' 
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'error' # Opcional: para que el flash sea rojo

# Callback para cargar usuario desde la sesión
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# REGISTRAR EL BLUEPRINT
# Le decimos a la app que use las rutas de 'auth_bp'
app.register_blueprint(auth_bp, url_prefix='/auth')

# Rutas de Juegos Protegidas

@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)


@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")


@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    flash('Juego agregado correctamente.', 'message')
    return redirect(url_for('juegos'))


@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)


@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(id, nombre, descripcion, precio)
    flash('Juego actualizado correctamente.', 'message')
    return redirect(url_for('juegos'))


@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    id = request.form["id"]
    controlador_juegos.eliminar_juego(id)
    flash('Juego eliminado correctamente.', 'message')
    return redirect(url_for('juegos'))


# --- Ejecutar la aplicación ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)