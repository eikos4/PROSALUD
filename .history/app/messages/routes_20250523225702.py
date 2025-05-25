from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Message, User

messages = Blueprint('messages', __name__, url_prefix='/messages')

@messages.route('/inbox')
@login_required
def inbox():
    convos = Message.get_user_conversations(current_user.id)
    return render_template('messages/inbox.html', convos=convos)

@messages.route('/chat/<int:other_id>', methods=['GET', 'POST'])
@login_required
def chat(other_id):
    other_user = User.query.get_or_404(other_id)
    if request.method == 'POST':
        text = request.form.get('text')
        if text and text.strip():
            msg = Message(
                sender_id=current_user.id,
                receiver_id=other_user.id,
                body=text.strip()
            )
            db.session.add(msg)
            db.session.commit()
            return redirect(url_for('messages.chat', other_id=other_id))
        else:
            flash("No puedes enviar un mensaje vacío.", "warning")
    convo = Message.get_conversation(current_user.id, other_user.id)
    return render_template(
        'messages/chat.html',
        convo=convo,
        other_user=other_user  # <--- Clave para el template
    )
