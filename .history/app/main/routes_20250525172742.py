# app/routes/main.py

from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from sqlalchemy import or_
from app.models import User
from app.forms import ContactForm  # Agrega este import si usas Flask-WTF

main = Blueprint('main', __name__)

# === Home / Landing page ===
@main.route('/')
def index():
    """Página principal de IndeWork."""
    return render_template('main/index.html')

# === Búsqueda de profesionales (público general) ===
@main.route('/search')
def search():
    """Búsqueda de usuarios/profesionales por nombre, categoría o descripción."""
    q = request.args.get('q', '')
    results = User.query.filter(
        or_(
            User.username.ilike(f'%{q}%'),
            User.category.ilike(f'%{q}%'),
            User.description.ilike(f'%{q}%')
        ),
        User.role == 'professional',      # SOLO profesionales
        User.active == True               # SOLO activos
    ).all()
    return render_template('main/search.html', query=q, results=results)

# === Perfil público profesional ===
@main.route('/professional/<int:id>')
@main.route('/perfil/<int:id>')  # Alias opcional, más amigable en español
def public_profile(id):
    """
    Vista de perfil público de un profesional.
    Solo muestra si el usuario está activo y es profesional.
    """
    user = User.query.get_or_404(id)
    if not user.active or user.role != 'professional':
        abort(404)
    return render_template('main/public_profile.html', user=user)

# === Página de términos y condiciones ===
@main.route('/terms')
def terms():
    """Términos y condiciones."""
    return render_template('main/terms.html')

# === Página de contacto ===
@main.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """
    Página de contacto. Usa WTForms para CSRF y validación.
    """
    form = ContactForm()
    if form.validate_on_submit():
        # Procesa el mensaje (por ejemplo, envía email o guarda en base de datos)
        flash('Tu mensaje fue enviado correctamente. Te responderemos pronto.', 'success')
        return redirect(url_for('main.contacto'))
    return render_template('main/contacto.html', form=form)

# === Listado público de profesionales ===
@main.route('/public_professionals')
def public_professionals():
    """
    Lista de todos los profesionales activos y visibles.
    """
    professionals = User.query.filter_by(role='professional', active=True).all()
    return render_template('main/public_professionals.html', professionals=professionals)
