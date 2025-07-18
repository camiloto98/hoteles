from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import pymysql
from app.config import Config
from app import bcrypt

# ✅ AÑADIDO: url_prefix='/' para que las rutas funcionen directo (ej: /registro)
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/')

def get_connection():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = bcrypt.generate_password_hash(request.form['contrasena']).decode('utf-8')

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)",
                           (nombre, correo, contrasena))
            conn.commit()
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('auth_bp.login'))
        except Exception as e:
            flash("Error al registrar: " + str(e), "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario and bcrypt.check_password_hash(usuario['contrasena'], contrasena):
            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash("Credenciales incorrectas", "danger")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for('auth_bp.login'))
