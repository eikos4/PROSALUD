# app/routes/main.py

from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from sqlalchemy import or_
from app.models import ContactMessage, User
from app import db
from flask import render_template, request
from sqlalchemy import or_
from app.models import User   # o la ruta correcta a tu modelo User

# Agrega este import si usas Flask-WTF
from app.forms import ContactForm
main = Blueprint('main', __name__)

# === Home / Landing page ===
# En tu ruta de index (ejemplo)
A
]

    return render_template('main/index.html', trending_services=trending_services)


# === Búsqueda de profesionales (público general) ===
@main.route('/search')
def search():
    q = request.args.get('q', '')

    # Filtrar profesionales por usuario, categoría o descripción, sin service_id
    results = User.query.filter(
        or_(
            User.username.ilike(f'%{q}%'),
            User.category.ilike(f'%{q}%'),
            User.description.ilike(f'%{q}%')
        ),
        User.role == 'professional',
        User.active == True
    ).all()

    # Renderizar sin pasar ningún 'servicio', solo resultados y la query
    return render_template('main/search.html',
                           query=q,
                           results=results)

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
    form = ContactForm()
    if form.validate_on_submit():
        # Guardar en la tabla
        mensaje = ContactMessage(
            nombre=form.nombre.data,
            email=form.email.data,
            mensaje=form.mensaje.data
        )
        db.session.add(mensaje)
        db.session.commit()
        flash('¡Tu mensaje fue enviado correctamente!', 'success')
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



