from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    nombre = session.get('usuario_nombre')  # Opcional: nombre del usuario si ha iniciado sesión
    return render_template('index.html', nombre=nombre)

@main_bp.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('dashboard.html', nombre=session['usuario_nombre'])

