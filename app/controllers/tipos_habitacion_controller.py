from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.tipo_habitacion_model import TipoHabitacionModel
import pymysql
from app.config import Config
from app import bcrypt

tipos_habitacion_bp = Blueprint('tipos_habitacion', __name__)

def get_connection():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )


@tipos_habitacion_bp.route('/tipos_habitacion')
def listar_tipos_habitacion():
    tipos = TipoHabitacionModel.obtener_todos()
    return render_template('listar.html', tipos=tipos)

@tipos_habitacion_bp.route('/tipos_habitacion/crear', methods=['GET', 'POST'])
def crear_tipo_habitacion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        TipoHabitacionModel.crear(nombre, descripcion)
        flash('Tipo de habitación creado correctamente')
        return redirect(url_for('tipos_habitacion.listar_tipos_habitacion'))
    return render_template('crear.html')

@tipos_habitacion_bp.route('/tipos_habitacion/editar/<int:id>', methods=['GET', 'POST'])
def editar_tipo_habitacion(id):
    tipo = TipoHabitacionModel.obtener_por_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        TipoHabitacionModel.actualizar(id, nombre, descripcion)
        flash('Tipo de habitación actualizado correctamente')
        return redirect(url_for('tipos_habitacion.listar_tipos_habitacion'))
    return render_template('editar.html', tipo=tipo)

@tipos_habitacion_bp.route('/tipos_habitacion/eliminar/<int:id>')
def eliminar_tipo_habitacion(id):
    TipoHabitacionModel.eliminar(id)
    flash('Tipo de habitación eliminado correctamente')
    return redirect(url_for('tipos_habitacion.listar_tipos_habitacion'))

@tipos_habitacion_bp.route('/tipos_habitacion/buscar', methods=['GET'])
def buscar_tipo_habitacion():
    criterio = request.args.get('criterio', '')
    tipos = TipoHabitacionModel.buscar_por_nombre_o_descripcion(criterio)
    return render_template('listar.html', tipos=tipos, criterio=criterio)
