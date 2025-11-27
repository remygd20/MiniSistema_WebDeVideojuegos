# Pruebas Unitarias - MiniSistema de Videojuegos

## Descripción
Este conjunto de pruebas verifica la integridad de los modelos, la seguridad de las rutas y el funcionamiento de la API RESTful utilizando unittest y una base de datos SQLite en memoria.

## Pruebas que se realizados

1.  Modelos (test_models.py):
    * Verificación de hashing de contraseñas (User).
    * Creación e inserción de registros en la base de datos (Juego).

2.  Rutas (test_routes.py):
    * Verificación de carga exitosa de páginas públicas (Login).
    * Verificación de protección de rutas: acceso no autorizado a /juegos redirige correctamente al login (Código 302).

3.  **API (test_api.py):
    * GET /api/juegos: Verifica respuesta 200 y formato JSON vacío al inicio.
    * POST /api/juegos: Verifica creación de recursos (Código 201) y persistencia de datos JSON.

## Retos y Soluciones
* Base de datos: Para no afectar la base de datos de producción (MySQL), se configuró setUp para usar sqlite:///:memory:.
* Codificación: Se ajustaron las pruebas de rutas para buscar palabras clave sin acentos como "Ingresar" para evitar errores de codificación (AssertionError) al leer el HTML.

## Ejecución
Para correr las pruebas:
python -m unittest discover -v tests