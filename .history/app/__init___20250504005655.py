# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Instancia tus extensiones aquí, UNA sola vez
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    # 1) Crea la app y carga configuración
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = 'hfgdhnftdyrtyufgimyuoi,yuimuimoyunrtbyetryvwetrwertwertbwerbtwert'  # ¡imprescindible!

    # 2) Inicializa las extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 3) Registra el user_loader de Flask-Login
    from app.models import User, Message
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 4) Importa y registra tus blueprints
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
