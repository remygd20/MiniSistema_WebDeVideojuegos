from flask_sqlalchemy import SQLAlchemy

# 1. Creamos el objeto db aquí, pero sin asociarlo a ninguna app todavía
db = SQLAlchemy()

# 2. El resto de la clase se queda exactamente igual
class Juego(db.Model):
    __tablename__ = 'juegos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Juego {self.nombre}>'