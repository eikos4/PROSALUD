from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Service, Request, Evaluation, Availability
from app.forms import ProfileForm, ServiceForm, AvailabilityForm, ResponseRequestForm

professional = Blueprint('professional', __name__, url_prefix='/professional')

# === DASHBOARD ===
@professional.route('/dashboard')
@login_required
def dashboard():
    from sqlalchemy import func
    solicitudes_count = Request.query.join(Service).filter(Service.professional_id == current_user.id).count()
    avg_rating = db.session.query(func.avg(Evaluation.rating)).filter(Evaluation.professional_id == current_user.id).scalar()
    avg_rating = round(avg_rating, 1) if avg_rating else '—'
    return render_template('professional/dashboard.html', solicitudes_count=solicitudes_count, avg_rating=avg_rating)

# === LISTAR Y CREAR SERVICIOS ===
@professional.route('/services', methods=['GET', 'POST'])
@login_required
def services():
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

# === EDITAR SERVICIO ===
@professional.route('/services/<int:service_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    if service.professional_id != current_user.id:
        abort(403)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.title = form.title.data
        service.description = form.description.data
        service.price = form.price.data
        db.session.commit()
        flash('Servicio actualizado exitosamente.', 'success')
        return redirect(url_for('professional.services'))
    return render_template('professional/edit_service.html', form=form, service=service)

# === ELIMINAR SERVICIO ===
@professional.route('/services/<int:service_id>/delete', methods=['POST'])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    if service.professional_id != current_user.id:
        abort(403)
    db.session.delete(service)
    db.session.commit()
    flash('Servicio eliminado exitosamente.', 'success')
    return redirect(url_for('professional.services'))

# === PERFIL PROFESIONAL ===
@professional.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
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

# === ELIMINAR DISPONIBILIDAD ===
@professional.route('/availability/delete/<int:id>', methods=['POST'])
@login_required
def delete_availability(id):
    slot = Availability.query.get_or_404(id)
    if slot.professional_id != current_user.id:
        flash('No tienes permiso para borrar esta disponibilidad.', 'danger')
        return redirect(url_for('professional.availability'))
    db.session.delete(slot)
    db.session.commit()
    flash('Disponibilidad eliminada correctamente.', 'success')
    return redirect(url_for('professional.availability'))

# Puedes agregar más rutas aquí a futuro

