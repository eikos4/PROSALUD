# config.py (en el mismo nivel que tu app.py)

import os

# Ruta absoluta al directorio de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clave secreta para formularios y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambia-esta-clave-por-una-muy-secreta'
    
    # URI de la base de datos; por ejemplo SQLite en desarrollo
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
