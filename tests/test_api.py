import unittest
import json
from app import app, db
from models import Juego

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_get_juegos_empty(self):
        """Prueba GET /api/juegos cuando no hay nada"""
        response = self.client.get('/api/juegos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, []) 

    def test_create_juego_api(self):
        """Prueba POST /api/juegos para crear uno"""
        nuevo_juego = {
            "nombre": "Zelda",
            "descripcion": "Aventura",
            "precio": 59.99
        }
        
        response = self.client.post('/api/juegos', 
                                    data=json.dumps(nuevo_juego),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201) 
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], 'Zelda')

if __name__ == '__main__':
    unittest.main()