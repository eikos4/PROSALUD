# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import User
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    # Flask por defecto busca templates en <root_path>/templates
    app = Flask(__name__)  

    # Carga tu configuración
    app.config.from_object('config.Config')

    # Inicializa extensiones
    db.init_app(app)
    login_manager.init_app(app)

     # Aquí registras el loader:
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registra blueprints...
    from app.auth.routes         import auth
    from app.main.routes         import main
    from app.professional.routes import professional
    from app.client.routes       import client
    from app.messages.routes     import messages

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(professional)
    app.register_blueprint(client)
    app.register_blueprint(messages)

    return app
