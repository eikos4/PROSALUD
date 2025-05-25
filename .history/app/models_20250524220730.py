from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# === MODELO DE USUARIO ===
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(150), unique=True, nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    active        = db.Column(db.Boolean, default=False, nullable=False)

    # Perfil profesional
    category      = db.Column(db.String(100), nullable=True)
    description   = db.Column(db.Text,       nullable=True)
    experience    = db.Column(db.Text,       nullable=True)
    location      = db.Column(db.String(100), nullable=True)
    role          = db.Column(db.String(20), nullable=False, default='client')

    # Relaciones de mensajes
    messages_sent     = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')

    # Servicios ofrecidos (como profesional)
    services = db.relationship('Service', backref='professional', lazy='dynamic', foreign_keys='Service.professional_id')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        if self.role == "professional":
            return self.active
        return True

    @is_active.setter
    def is_active(self, value):
        self.active = value

# === MODELO DE MENSAJE ===
class Message(db.Model):
    __tablename__ = 'message'
    id          = db.Column(db.Integer, primary_key=True)
    sender_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body        = db.Column(db.Text, nullable=False)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id} to {self.receiver_id}>'

    @staticmethod
    def get_conversation(user_id, other_id):
        return Message.query.filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == other_id)) |
            ((Message.sender_id == other_id) & (Message.receiver_id == user_id))
        ).order_by(Message.timestamp).all()

    @staticmethod
    def get_user_conversations(user_id):
        return Message.query.filter(
            (Message.sender_id == user_id) | (Message.receiver_id == user_id)
        ).order_by(Message.timestamp.desc()).all()

# === MODELO DE SERVICIO OFRECIDO ===
class Service(db.Model):
    __tablename__ = 'service'
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(120), nullable=False)
    description     = db.Column(db.Text)
    price           = db.Column(db.Float, nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # <-- ¡Un solo FK aquí!

    # Relación de solicitudes (requests)
    requests = db.relationship('Request', backref='service', lazy='dynamic')

# === MODELO DE SOLICITUD (REQUEST) ===
class Request(db.Model):
    __tablename__ = 'request'
    id            = db.Column(db.Integer, primary_key=True)
    client_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id    = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date_requested= db.Column(db.DateTime, default=datetime.utcnow)
    status        = db.Column(db.String(20), default="pending")
    message       = db.Column(db.Text)

    # Relaciones explícitas
    client   = db.relationship('User', foreign_keys=[client_id])
    # service  = db.relationship('Service', foreign_keys=[service_id])  # NO necesario, lo tienes como backref arriba

# === MODELO DE DISPONIBILIDAD ===
class Availability(db.Model):
    __tablename__ = 'availability'
    id               = db.Column(db.Integer, primary_key=True)
    professional_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weekday          = db.Column(db.String(10), nullable=False)
    start_time       = db.Column(db.Time, nullable=False)
    end_time         = db.Column(db.Time, nullable=False)

# === MODELO DE EVALUACIÓN ===
class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    id              = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating          = db.Column(db.Integer, nullable=False)
    comment         = db.Column(db.Text, nullable=True)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    # Relaciones opcionales:
    professional = db.relationship('User', foreign_keys=[professional_id], backref='received_evaluations')
    client = db.relationship('User', foreign_keys=[client_id])

