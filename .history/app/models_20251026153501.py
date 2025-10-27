# app/models.py
from datetime import datetime
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# ============================================================
# 🧍 MODELO DE USUARIO
# ============================================================



# ============================================================
# 💬 MODELO DE MENSAJE
# ============================================================

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    service = db.relationship('Service', backref='messages')

    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id} to {self.receiver_id}>'

    @staticmethod
    def get_conversation(user_id, other_id, service_id):
        """Obtiene todos los mensajes entre dos usuarios para un servicio."""
        return Message.query.filter(
            (((Message.sender_id == user_id) & (Message.receiver_id == other_id)) |
             ((Message.sender_id == other_id) & (Message.receiver_id == user_id))) &
            (Message.service_id == service_id)
        ).order_by(Message.timestamp).all()

    @staticmethod
    def get_user_conversations_grouped(user_id):
        """Agrupa conversaciones por usuario y servicio."""
        from sqlalchemy import or_, desc
        msgs = Message.query.filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id)
        ).order_by(desc(Message.timestamp)).all()

        grouped = {}
        for msg in msgs:
            other = msg.receiver_user if msg.sender_id == user_id else msg.sender_user
            key = (other.id, msg.service_id)
            if key not in grouped:
                grouped[key] = {
                    'other': other,
                    'service': msg.service,
                    'last_msg': msg
                }
        return sorted(grouped.values(), key=lambda x: x['last_msg'].timestamp, reverse=True)

# ============================================================
# 💼 MODELO DE SERVICIO
# ============================================================

class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    requests = db.relationship('Request', backref='service', lazy='dynamic')

    def __repr__(self):
        return f'<Service {self.title}>'

# ============================================================
# 📩 MODELO DE SOLICITUD
# ============================================================

class Request(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date_requested = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")
    message = db.Column(db.Text)

    client = db.relationship('User', foreign_keys=[client_id])

    def __repr__(self):
        return f'<Request {self.id} - {self.status}>'

# ============================================================
# ⏰ MODELO DE DISPONIBILIDAD
# ============================================================

class Availability(db.Model):
    __tablename__ = 'availability'

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weekday = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<Availability {self.weekday} {self.start_time}-{self.end_time}>'

# ============================================================
# ⭐ MODELO DE EVALUACIÓN
# ============================================================

class Evaluation(db.Model):
    __tablename__ = 'evaluation'

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))

    def __repr__(self):
        return f'<Evaluation {self.rating}★ for professional {self.professional_id}>'

# ============================================================
# 📬 MODELO DE MENSAJE DE CONTACTO
# ============================================================

class ContactMessage(db.Model):
    __tablename__ = 'contact_message'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage from {self.email}>'
