# app/models.py


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash  # <- importa estas

from app import db 

# app/models.py


from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id             = db.Column(db.Integer, primary_key=True)
    username       = db.Column(db.String(150), unique=True, nullable=False)
    email          = db.Column(db.String(150), unique=True, nullable=False)
    password_hash  = db.Column(db.String(256), nullable=False)
    active         = db.Column(db.Boolean, default=False, nullable=False)  # <— nuevo campo

    # relaciones mensajes...
    messages_sent     = db.relationship('Message', foreign_keys='Message.sender_id',
                                        backref='sender', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id',
                                        backref='receiver', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        # Flask-Login usa esta propiedad para saber si puede iniciar sesión
        return self.active

    # Opcionalmente, puedes añadir un setter para ser más explícito:
    @is_active.setter
    def is_active(self, value):
        self.active = value


class Message(db.Model):
    __tablename__ = 'message'
    id          = db.Column(db.Integer, primary_key=True)
    sender_id   = db.Column(db.Integer, db.ForeignKey('user.id'),   nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'),   nullable=False)
    body        = db.Column(db.Text,    nullable=False)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id} to {self.receiver_id}>'

    @staticmethod
    def get_conversation(user_id, other_id):
        """Devuelve todos los mensajes entre user_id y other_id ordenados por timestamp."""
        return Message.query.filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == other_id)) |
            ((Message.sender_id == other_id) & (Message.receiver_id == user_id))
        ).order_by(Message.timestamp).all()

    @staticmethod
    def get_user_conversations(user_id):
        """
        Devuelve las últimas conversaciones de user_id, agrupando por interlocutor.
        (Para simplificar, aquí devolvemos todos los mensajes recibidos y enviados).
        """
        return Message.query.filter(
            (Message.sender_id == user_id) | (Message.receiver_id == user_id)
        ).order_by(Message.timestamp.desc()).all()
