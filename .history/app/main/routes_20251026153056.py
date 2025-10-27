# app/routes/main.py

from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from sqlalchemy import or_
from app.models import ContactMessage, User
from app import db
from flask import render_template, request
from sqlalchemy import or_
from app.models import User   # o la ruta correcta a tu modelo User
from app.models import Evaluation
from flask_login import current_user, login_required


# Agrega este import si usas Flask-WTF
from app.forms import ContactForm
main = Blueprint('main', __name__)

# === Home / Landing page ===
# En tu ruta de index (ejemplo)
@main.route('/')
def index():
    trending_services = [
        'Médico General', 'Psicólogo', 'Nutricionista', 'Kinesiólogo', 'Fonoaudiólogo',
        'Terapeuta Ocupacional', 'Psiquiatra', 'Psicopedagogo', 'Podólogo', 'Enfermero a Domicilio',
        'Técnico en Enfermería', 'Matrona', 'Dentista', 'Oftalmólogo', 'Ginecólogo',
        'Cardiólogo', 'Dermatólogo', 'Neurólogo', 'Urólogo', 'Geriatra',
        'Rehabilitación Física', 'Consultas Médicas Online', 'Consulta Pediátrica',
        'Apoyo Emocional', 'Orientación Psicológica', 'Terapia Familiar',
        'Terapia de Pareja', 'Educador en Salud', 'Coaching en Salud', 'Medicina Integrativa',
        'Homeópata', 'Masajista Terapéutico', 'Fisioterapeuta', 'Osteópata', 'Acupunturista'
]

    return render_template('main/index.html', trending_services=trending_services)


# === Búsqueda de profesionales (público general) ===
@main.route('/search')
def search():
    from sqlalchemy import func
    q = request.args.get('q', '')

    # Obtener todas las categorías con profesionales activos
    categories = db.session.query(User.category).filter(
        User.role == 'professional',
        User.active == True,
        User.category.isnot(None)
    ).distinct().all()

    top_professionals = {}
    for (cat,) in categories:
        top_professionals[cat] = (
            User.query.filter_by(category=cat, active=True, role='professional')
            .order_by(User.rating.desc().nullslast())  # si tienes campo rating
            .limit(3)
            .all()
        )

    return render_template('main/search.html',
                           query=q,
                           top_professionals=top_professionals)

# === Perfil público profesional ===
@main.route('/professional/<int:id>')
@main.route('/perfil/<int:id>')
def public_profile(id):
    """
    Perfil público de un profesional: datos + reseñas.
    """
    user = User.query.get_or_404(id)
    if not user.active or user.role != 'professional':
        abort(404)

    # Obtener todas las reseñas recibidas
    reviews = Evaluation.query.filter_by(professional_id=user.id).order_by(Evaluation.created_at.desc()).all()

    return render_template('main/public_profile.html', user=user, reviews=reviews)


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



