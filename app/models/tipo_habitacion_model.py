from flask import current_app
import pymysql
from app.config import Config
from app import bcrypt

class TipoHabitacionModel:
    
    @staticmethod
    def get_connection():
        return pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )

    @staticmethod
    def obtener_todos():
        conn = TipoHabitacionModel.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tipos_habitacion")
            return cursor.fetchall()

    @staticmethod
    def obtener_por_id(id):
        conn = TipoHabitacionModel.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tipos_habitacion WHERE id = %s", (id,))
            return cursor.fetchone()

    @staticmethod
    def crear(nombre, descripcion):
        conn = TipoHabitacionModel.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO tipos_habitacion (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        conn.commit()

    @staticmethod
    def actualizar(id, nombre, descripcion):
        conn = TipoHabitacionModel.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE tipos_habitacion SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id))
        conn.commit()

    @staticmethod
    def eliminar(id):
        conn = TipoHabitacionModel.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tipos_habitacion WHERE id = %s", (id,))
        conn.commit()

    @staticmethod
    def buscar_por_nombre_o_descripcion(criterio):
        conn = TipoHabitacionModel.get_connection()
        with conn.cursor() as cursor:
            consulta = """
                SELECT * FROM tipos_habitacion 
                WHERE nombre LIKE %s OR descripcion LIKE %s
            """
            like_criterio = f"%{criterio}%"
            cursor.execute(consulta, (like_criterio, like_criterio))
            return cursor.fetchall()
