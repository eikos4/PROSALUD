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


