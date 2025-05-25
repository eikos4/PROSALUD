# config.py (en el mismo nivel que tu app.py)

import os

# Ruta absoluta al directorio de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clave secreta para formularios y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5687658758765876876tuytjytufjhfjhgfhghgr5e4654767676568itykutiuy'
    
    # URI de la base de datos; por ejemplo SQLite en desarrollo
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
