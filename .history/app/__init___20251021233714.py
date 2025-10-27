# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect      # ← Importar aquí


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()    
   # ← Instanciar aquí

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config.from_object('config.Config')
    # (SECRET_KEY ya se carga desde Config)

    # Inicializa las extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)                 # ← Iniciar CSRFProtect

    # user_loader, blueprints, etc...
    from app.models import User, Message
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes         import auth
    from app.main.routes         import main
    from app.professional.routes import professional
    from app.client.routes       import client
    from app.messages.routes     import messages
    from app.admin       import admin # pyright: ignore[reportMissingImports]


    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(professional)
    app.register_blueprint(client)
    app.register_blueprint(messages)
    app.register_blueprint(admin)


    return app
