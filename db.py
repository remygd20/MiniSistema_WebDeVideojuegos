import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='hola1234*',
            database='juegos'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la BD: {e}")
        return None