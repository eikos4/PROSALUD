from flask import Blueprint, abort, render_template, request
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

from sqlalchemy import or_

@main.route('/search')
def search():
    q = request.args.get('q', '')
    results = User.query.filter(
        or_(
            User.username.ilike(f'%{q}%'),
            User.category.ilike(f'%{q}%'),
            User.description.ilike(f'%{q}%')
        )
    ).all()
    return render_template('main/search.html', query=q, results=results)





# ← Nueva ruta para perfil público
@main.route('/professional/<int:id>')
def public_profile(id):
    user = User.query.get_or_404(id)
    # Solo mostramos profesionales activos
    if not user.is_active:
        abort(404)
    return render_template('main/public_profile.html', user=user)


@main.route('/public_professionals')
def public_professionals():
    professionals = User.query.filter_by(role='professional', active=True).all()
    return render_template('public_professionals.html', professionals=professionals)


@main.route('/terms')
def terms():
    return render_template('terms.html')
