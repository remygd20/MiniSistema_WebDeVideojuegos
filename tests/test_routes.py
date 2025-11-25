import unittest
from app import app, db

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_login_page_loads(self):
        """Prueba que la página de login cargue (código 200)"""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        # CORRECCIÓN: Buscamos 'Ingresar' que sí está en el botón y no tiene acentos problemáticos
        self.assertIn(b'Ingresar', response.data)

    def test_protected_route_redirect(self):
        """Prueba que entrar a /juegos sin loguearse te mande al login"""
        # Intentamos entrar a /juegos sin haber iniciado sesión
        response = self.client.get('/juegos')
        
        # 302 significa redirección (Found/Redirect)
        self.assertEqual(response.status_code, 302)
        # Verificamos que nos mande a /auth/login
        self.assertIn('/auth/login', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()