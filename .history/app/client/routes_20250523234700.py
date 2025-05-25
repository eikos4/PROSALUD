from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import User

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/dashboard')
@login_required
def dashboard():
    # Parámetros de búsqueda y filtro
    q      = request.args.get('q', '').strip()
    region = request.args.get('region', '').strip()

    # Consulta base: solo profesionales activos
    query = User.query.filter_by(role='professional', active=True)

    if q:
        query = query.filter(User.username.ilike(f'%{q}%'))
    if region:
        query = query.filter(User.location == region)

    professionals = query.all()

    # Obtener lista única de regiones
    regions = sorted({
        u.location for u in User.query.with_entities(User.location).distinct() 
        if u.location
    })

    return render_template(
        'client/dashboard.html',
        professionals=professionals,
        regions=regions,
        selected_region=region,
        search_term=q
    )


