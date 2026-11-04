from flask import Flask
from app.database import db, migrate

def create_app():
    app = Flask(__name__)
    
    # Configuraciones
    app.config['SECRET_KEY'] = 'clave_secreta_super_segura'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_anuncios.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # IMPORTANTE: Importar los modelos aquí para que la base de datos los reconozca
    from app import models
    
    # Registrar Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app