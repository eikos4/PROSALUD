# app/routes/main.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import current_user
from sqlalchemy import or_, func
from app import db
from app.models import User, Evaluation, ContactMessage
from app.forms import ContactForm

main = Blueprint('main', __name__)

# === 🏠 HOME / LANDING PAGE ===
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


# === 🔍 BÚSQUEDA DE PROFESIONALES ===
@main.route('/search')
def search():
    from sqlalchemy import func

    q = request.args.get('q', '').strip()
    region = request.args.get('region', '').strip()
    category_filter = request.args.get('category', '').strip()

    # 🔹 Mismas categorías del index
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

    # Base query de profesionales activos
    base_query = User.query.filter(
        User.role == 'professional',
        User.active == True
    )

    if q:
        base_query = base_query.filter(
            or_(
                User.username.ilike(f'%{q}%'),
                User.full_name.ilike(f'%{q}%'),
                User.category.ilike(f'%{q}%'),
                User.subcategory.ilike(f'%{q}%'),
                User.description.ilike(f'%{q}%')
            )
        )

    if region:
        base_query = base_query.filter(User.location.ilike(f'%{region}%'))
    if category_filter:
        base_query = base_query.filter(User.category == category_filter)

    # Obtener top profesionales por categoría
    categories = db.session.query(User.category).filter(
        User.role == 'professional', User.active == True, User.category.isnot(None)
    ).distinct().all()

    top_professionals[cat] = [
        row[0] for row in (
            base_query.filter(User.category == cat)
            .outerjoin(Evaluation, Evaluation.professional_id == User.id)
            .add_columns(func.coalesce(func.avg(Evaluation.rating), 0).label('avg_rating'))
            .group_by(User.id)
            .order_by(func.coalesce(func.avg(Evaluation.rating), 0).desc())
            .limit(3)
            .all()
        )
    ]


    return render_template(
        'main/search.html',
        query=q,
        region=region,
        category_filter=category_filter,
        trending_services=trending_services,
        top_professionals=top_professionals
    )



# === 👩‍⚕️ PERFIL PÚBLICO PROFESIONAL ===
@main.route('/professional/<int:id>')
@main.route('/perfil/<int:id>')
def public_profile(id):
    """
    Muestra el perfil público de un profesional y sus reseñas.
    """
    user = User.query.get_or_404(id)
    if not user.active or user.role != 'professional':
        abort(404)

    reviews = (
        Evaluation.query
        .filter_by(professional_id=user.id)
        .order_by(Evaluation.created_at.desc())
        .all()
    )

    avg_rating = (
        db.session.query(func.avg(Evaluation.rating))
        .filter(Evaluation.professional_id == user.id)
        .scalar()
    )
    avg_rating = round(avg_rating, 1) if avg_rating else None

    return render_template(
        'main/public_profile.html',
        user=user,
        reviews=reviews,
        avg_rating=avg_rating
    )


# === 📜 TÉRMINOS Y CONDICIONES ===
@main.route('/terms')
def terms():
    return render_template('main/terms.html')


# === 💬 CONTACTO ===
@main.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactForm()
    if form.validate_on_submit():
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


# === 📋 LISTADO PÚBLICO DE PROFESIONALES ===
@main.route('/public_professionals')
def public_professionals():
    professionals = (
        User.query.filter_by(role='professional', active=True)
        .order_by(User.id.desc())
        .all()
    )
    return render_template('main/public_professionals.html', professionals=professionals)
