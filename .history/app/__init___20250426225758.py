from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__,
                template_folder='app/templates',
                static_folder='app/static')
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Importar y registrar Blueprints
    from app.auth.routes import auth
    from app.main.routes import main
    from app.professional.routes import professional
    from app.client.routes import client
    from app.messages.routes import messages

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(professional)
    app.register_blueprint(client)
    app.register_blueprint(messages)

    return app
