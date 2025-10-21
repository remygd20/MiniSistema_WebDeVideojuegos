from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Se crea la instancia de SQLAlchemy que se conectará a la app
db = SQLAlchemy()

# Modelo para la tabla juegos
class Juego(db.Model):
    __tablename__ = 'juegos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    # Representación del objeto en string, útil para debugging
    def __repr__(self):
        return f'<Juego {self.nombre}>'


# Modelo User
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) 

    # Password que no es legible
    @property
    def password(self):
        raise AttributeError('La contraseña no es un atributo legible.')

    # Setter para el password que genera el hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Método para verificar el hash
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'