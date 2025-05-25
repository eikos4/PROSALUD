# app/models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id             = db.Column(db.Integer, primary_key=True)
    username       = db.Column(db.String(150), unique=True, nullable=False)
    email          = db.Column(db.String(150), unique=True, nullable=False)
    password_hash  = db.Column(db.String(256), nullable=False)
    # Relaciones con mensajes
    messages_sent     = db.relationship(
        'Message',
        foreign_keys='Message.sender_id',
        backref='sender',
        lazy='dynamic'
    )
    messages_received = db.relationship(
        'Message',
        foreign_keys='Message.receiver_id',
        backref='receiver',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

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
