import unittest
from app import app, db
from models import User, Juego

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        """Se ejecuta ANTES de cada prueba"""
        # Configuramos la app para testeo y usamos BD en memoria (SQLite)
        # Esto evita borrar tus datos reales de MySQL
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Desactivar CSRF para facilitar tests
        
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Crea las tablas en la BD de memoria
        db.create_all()

    def tearDown(self):
        """Se ejecuta DESPUÉS de cada prueba"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """Prueba que las contraseñas se encripten y verifiquen bien"""
        u = User(username='testuser')
        u.password = 'gatito'
        
        self.assertTrue(u.verify_password('gatito'))
        self.assertFalse(u.verify_password('perrito'))

    def test_juego_creation(self):
        """Prueba que se pueda crear y guardar un juego"""
        j = Juego(nombre='Mario', descripcion='Platformer', precio=50.0)
        db.session.add(j)
        db.session.commit()
        
        # Verificamos que se haya guardado (ID debe ser 1)
        self.assertEqual(Juego.query.count(), 1)
        self.assertEqual(Juego.query.first().nombre, 'Mario')

if __name__ == '__main__':
    unittest.main()