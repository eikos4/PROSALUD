from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import User

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/dashboard')
@login_required
def dashboard():
    # En la versión inicial, podrías reutilizar la búsqueda
    return render_template('client/dashboard.html')
