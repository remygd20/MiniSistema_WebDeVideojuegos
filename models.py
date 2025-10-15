from flask_sqlalchemy import SQLAlchemy

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
