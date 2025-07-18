from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    from app.config import Config
    app.config.from_object(Config)
    bcrypt.init_app(app)

    # Registrar rutas
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.controllers.tipos_habitacion_controller import tipos_habitacion_bp
    
  
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(tipos_habitacion_bp)
    
    return app
