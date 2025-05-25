from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import User

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/dashboard')
@login_required
def dashboard():
    # En la versión inicial, podrías reutilizar la búsqueda
    return render_template('client/dashboard.html')



# app/client/routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import User

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/dashboard')
@login_required
def dashboard():
    # Recogemos filtros desde la query string
    q      = request.args.get('q', '').strip()
    region = request.args.get('region', '').strip()

    # Construir la consulta base: solo profesionales
    query = User.query.filter_by(role='professional')

    # Filtrado por término
    if q:
        query = query.filter(User.username.ilike(f'%{q}%'))

    # Filtrado por región (asume que User tiene campo 'location')
    if region:
        query = query.filter(User.location == region)

    professionals = query.all()

    # Lista de regiones para el filtro
    regions = sorted({u.location for u in User.query.with_entities(User.location).distinct() if u.location})

    return render_template(
        'client/dashboard.html',
        professionals=professionals,
        regions=regions,
        selected_region=region,
        search_term=q
    )
