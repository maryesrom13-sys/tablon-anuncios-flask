from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Usuario, Categoria, Anuncio
from app.database import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('base.html')

@main_bp.route('/registros', methods=['GET', 'POST'])
def registros():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado', 'danger')
            return redirect(url_for('main.registros'))

        nuevo_usuario = Usuario(nombre=nombre, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))

    return render_template('registros.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.password == password:
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html')

@main_bp.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        
        cat_existente = Categoria.query.filter_by(nombre=nombre).first()
        if cat_existente:
            flash('La categoría ya existe', 'danger')
            return redirect(url_for('main.categorias'))

        nueva_categoria = Categoria(nombre=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()

        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('main.categorias'))

    lista_categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=lista_categorias)

# NUEVA RUTA PARA ANUNCIOS
@main_bp.route('/anuncios', methods=['GET', 'POST'])
def anuncios():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        categoria_id = request.form.get('categoria_id')

        nuevo_anuncio = Anuncio(
            titulo=titulo,
            descripcion=descripcion,
            categoria_id=categoria_id
        )
        db.session.add(nuevo_anuncio)
        db.session.commit()

        flash('Anuncio publicado con éxito', 'success')
        return redirect(url_for('main.anuncios'))

    lista_anuncios = Anuncio.query.all()
    lista_categorias = Categoria.query.all()
    return render_template('anuncios.html', anuncios=lista_anuncios, categorias=lista_categorias)