from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Service, Request, Evaluation, Availability
from app.forms import ProfileForm, ServiceForm, AvailabilityForm, ResponseRequestForm
from app.routes.professional import professional

professional = Blueprint('professional', __name__, url_prefix='/professional')

# === DASHBOARD ===
@professional.route('/dashboard')
@login_required
def dashboard():
    solicitudes_count = Request.query.join(Service).filter(Service.professional_id == current_user.id).count()
    # Calcular promedio de rating (puedes mejorar este query)
    from sqlalchemy import func
    avg_rating = db.session.query(func.avg(Evaluation.rating)).filter(Evaluation.professional_id == current_user.id).scalar()
    avg_rating = round(avg_rating, 1) if avg_rating else '—'
    return render_template('professional/dashboard.html', solicitudes_count=solicitudes_count, avg_rating=avg_rating)


@professional.route('/services', methods=['GET', 'POST'])
@login_required
def services():
    # Mostrar los servicios creados por el profesional
    services = Service.query.filter_by(professional_id=current_user.id).all()
    form = ServiceForm()
    if form.validate_on_submit():
        new_service = Service(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            professional_id=current_user.id
        )
        db.session.add(new_service)
        db.session.commit()
        flash('Servicio creado exitosamente.', 'success')
        return redirect(url_for('professional.services'))
    return render_template('professional/services.html', services=services, form=form)




# === PERFIL PROFESIONAL ===
@professional.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        # Ajusta nombre de campo si lo cambiaste en el modelo
        current_user.username    = form.full_name.data
        current_user.category    = form.category.data
        current_user.description = form.description.data
        current_user.experience  = form.experience.data
        db.session.commit()
        flash('Perfil actualizado.', 'success')
        return redirect(url_for('professional.dashboard'))
    return render_template('professional/profile.html', form=form)

# === ACTIVAR PERFIL / PAGO ===
@professional.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        current_user.active = True
        db.session.commit()
        flash('Pago realizado. Tu perfil está activo.', 'success')
        return redirect(url_for('professional.dashboard'))
    return render_template('professional/payment.html')

# === 1. VER SOLICITUDES RECIBIDAS ===
@professional.route('/requests')
@login_required
def requests_list():
    solicitudes = Request.query\
        .join(Service)\
        .filter(Service.professional_id == current_user.id)\
        .order_by(Request.date_requested.desc()).all()
    return render_template('professional/requests.html', solicitudes=solicitudes)

# === 2. RESPONDER SOLICITUD ===
@professional.route('/requests/<int:request_id>/respond', methods=['GET', 'POST'])
@login_required
def respond_request(request_id):
    req = Request.query.get_or_404(request_id)
    form = ResponseRequestForm()
    if form.validate_on_submit():
        req.status = form.status.data  # accepted/rejected
        db.session.commit()
        flash('Solicitud respondida correctamente.', 'success')
        return redirect(url_for('professional.requests_list'))
    return render_template('professional/respond_request.html', form=form, req=req)

# === 3. HISTORIAL DE SERVICIOS COMPLETADOS ===
@professional.route('/history')
@login_required
def history():
    servicios = Request.query\
        .join(Service)\
        .filter(Service.professional_id == current_user.id, Request.status == "completed")\
        .order_by(Request.date_requested.desc()).all()
    return render_template('professional/history.html', servicios=servicios)

# === 4. VER EVALUACIONES RECIBIDAS ===
@professional.route('/reviews')
@login_required
def reviews():
    evaluaciones = Evaluation.query.filter_by(professional_id=current_user.id).all()
    return render_template('professional/reviews.html', evaluaciones=evaluaciones)

# === 5. CONFIGURAR DISPONIBILIDAD ===
@professional.route('/availability', methods=['GET', 'POST'])
@login_required
def availability():
    form = AvailabilityForm()
    if form.validate_on_submit():
        nueva = Availability(
            professional_id=current_user.id,
            weekday=form.weekday.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Disponibilidad agregada.', 'success')
        return redirect(url_for('professional.availability'))
    disponibles = Availability.query.filter_by(professional_id=current_user.id).all()
    return render_template('professional/availability.html', form=form, disponibles=disponibles)


from flask import redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Availability

@professional.route('/availability/delete/<int:id>', methods=['POST'])
@login_required
def delete_availability(id):
    slot = Availability.query.get_or_404(id)
    # Opcional: valida que solo el dueño puede borrar
    if slot.professional_id != current_user.id:
        flash('No tienes permiso para borrar esta disponibilidad.', 'danger')
        return redirect(url_for('professional.availability'))
    db.session.delete(slot)
    db.session.commit()
    flash('Disponibilidad eliminada correctamente.', 'success')
    return redirect(url_for('professional.availability'))


# Puedes agregar más rutas aquí a futuro
# === 6. CREAR O EDITAR SERVICIO ===
