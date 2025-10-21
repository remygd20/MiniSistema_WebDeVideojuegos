from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Juego, User  # Importar User
import controlador_juegos
from forms import LoginForm, RegistrationForm  # Importar formularios
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash # Para registrar

app = Flask(__name__)

# Configuración de la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola1234*@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Clave secreta para sesiones y WTForms
app.config['SECRET_KEY'] = 'mi-clave-secreta-muy-segura-12345'

# Se inicializa la base de datos con la configuración de la app
db.init_app(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Vista a la que se redirige si no está logueado
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.' # Mensaje flash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Rutas de Autenticación ---

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Usuario o contraseña inválidos', 'error') # Categoría 'error'
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        flash('Has iniciado sesión exitosamente.', 'message') # Categoría 'message'
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('juegos'))

    return render_template('login.html', form=form)


@app.route("/logout")
@login_required 
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'message')
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('¡Felicidades, te has registrado exitosamente! Ahora puedes iniciar sesión.', 'message')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# --- Rutas de Juegos (Protegidas) ---

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
        # db.create_all() creará la tabla 'users' si no existe
        db.create_all()
    app.run(port=8000, debug=True)