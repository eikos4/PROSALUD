# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    # 1) Instancia la app, apuntando a tus carpetas de templates/static
    app = Flask(
        __name__,
        template_folder='app/templates',
        static_folder='app/static'
    )

    # 2) Aquí cargas tu configuración desde config.py
    #    <<<---- Agrega esta línea justo aquí:
    app.config.from_object('config.Config')

    # 3) Inicializas extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # 4) Registras blueprints
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
