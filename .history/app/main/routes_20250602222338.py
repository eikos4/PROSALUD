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
@main.route('/')
def index():
    trending_services = [
    'Diseño Web', 'Abogados', 'Clases de Yoga', 'Contabilidad', 'Desarrollador App', 'Psicólogo',
    'Análisis Comercial', 'Asesoría Laboral', 'Redacción y Copywriting', 'Marketing Digital',
    'Community Manager', 'Fotografía Profesional', 'Asesoría Legal', 'Clases de Música',
    'Clases Particulares', 'Nutricionista', 'Masajista', 'Electricista', 'Gasfiter', 'Carpintero',
    'Mecánico Automotriz', 'Cerrajero', 'Arquitectura', 'Decorador de Interiores', 'Personal Trainer',
    'Entrenador Personal', 'Traductor', 'Diseño Gráfico', 'Editor de Video', 'Desarrollador WordPress',
    'Soporte Técnico', 'Reparación de PC', 'Peluquería y Barbería', 'Manicurista', 'Podólogo',
    'Asesor Financiero', 'Corredor de Propiedades', 'Coaching Profesional', 'Terapeuta Holístico',
    'Psicopedagogo', 'Preparador Físico', 'Fonoaudiólogo', 'Tatuador', 'Desarrollador Freelance',
    'Consultor SAP', 'Abogado Laboral', 'Ingeniero Eléctrico', 'Clases de Inglés', 'Maestro de Construcción',
    'Instalador de Paneles Solares', 'Consultor en Seguridad', 'Ilustrador', 'Profesor de Matemática',
    'Asesor en Recursos Humanos', 'Consultor en UX/UI', 'Técnico en Climatización', 'Asistente Virtual',
    'Gestor de Proyectos', 'Animador Digital', 'Coach de Vida', 'Dietista', 'Psicólogo Infantil',
    'Enfermero a Domicilio', 'Logopeda', 'Técnico en Redes', 'Asesor en Comercio Exterior',
    'Desarrollador de e-Commerce', 'Diseñador de Moda', 'Asesor Previsional', 'Profesor de Programación'
]

    return render_template('main/index.html', trending_services=trending_services)


# === Búsqueda de profesionales (público general) ===
@main.route('/search')
def search():
    # 1) Obtén service_id desde la querystring
    try:
        service_id = int(request.args.get('service_id', ''))
    except ValueError:
        abort(400)  # parámetro mal formado

    # 2) Carga el servicio o 404 si no existe
    service = Service.query.get_or_404(service_id)

    # 3) Obtén la cadena de búsqueda
    q = request.args.get('q', '')

    # 4) Filtra profesionales en ese servicio
    results = User.query.filter(
        or_(
            User.username.ilike(f'%{q}%'),
            User.category.ilike(f'%{q}%'),
            User.description.ilike(f'%{q}%')
        ),
        User.role == 'professional',
        User.active == True,
        User.services.contains(service)  # o la relación que tengas para “servicio”
    ).all()

    # 5) Renderiza pasando BOTH `results` y `service` al template
    return render_template('main/search.html',
                           query=q,
                           results=results,
                           servicio=service)

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



