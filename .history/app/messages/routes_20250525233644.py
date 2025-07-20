# messages/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Message, User, Service
from app.forms import MessageForm

messages = Blueprint('messages', __name__, url_prefix='/messages')

# --- Bandeja de entrada agrupada por usuario y servicio ---
@messages.route('/inbox')
@login_required
def inbox():
    # Usamos el método pro del modelo Message
    grouped_convos = Message.get_user_conversations_grouped(current_user.id)
    return render_template('messages/inbox.html', grouped_convos=grouped_convos)

# --- Chat directo, separado por usuario y servicio ---
@messages.route('/chat/<int:other_id>/<int:service_id>', methods=['GET', 'POST'])
@login_required
def chat(other_id, service_id):
    other_user = User.query.get_or_404(other_id)
    service = Service.query.get_or_404(service_id)
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            receiver_id=other_user.id,
            body=form.body.data.strip(),
            service_id=service.id
        )
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('messages.chat', other_id=other_id, service_id=service_id))
    # Solo los mensajes entre estos dos usuarios y este servicio
    convo = Message.query.filter_by(service_id=service_id).filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == other_id)) |
        ((Message.sender_id == other_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()
    return render_template('messages/chat.html', convo=convo, form=form, other_user=other_user, service=service)
