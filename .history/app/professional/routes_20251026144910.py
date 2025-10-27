# app/routes/professional.py

from flask import (
    Blueprint, render_template, redirect, url_for, flash, request,
    abort, send_from_directory, current_app
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func
import os


from app.models import User, Service, Request, Evaluation, Availability
from app.forms import (
    ProfileForm, ServiceForm, AvailabilityForm,
    ResponseRequestForm, DeleteForm
)

# -------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# -------------------------------------------------------

professional = Blueprint('professional', __name__, url_prefix='/professional')

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads/certificates')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------------
# DASHBOARD PROFESIONAL
# -------------------------------------------------------

@professional.route('/dashboard')
@login_required
def dashboard():
    solicitudes_count = (
        Request.query.join(Service)
        .filter(Service.professional_id == current_user.id)
        .count()
    )
    avg_rating = (
        db.session.query(func.avg(Evaluation.rating))
        .filter(Evaluation.professional_id == current_user.id)
        .scalar()
    )
    avg_rating = round(avg_rating, 1) if avg_rating else '—'
    return render_template(
        'professional/dashboard.html',
        solicitudes_count=solicitudes_count,
        avg_rating=avg_rating
    )

# -------------------------------------------------------
# GESTIÓN DE SERVICIOS
# -------------------------------------------------------

@professional.route('/services', methods=['GET', 'POST'])
@login_required
def services():
    services = Service.query.filter_by(professional_id=current_user.id).all()
    form = ServiceForm()
    delete_form = DeleteForm()

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

    return render_template(
        'professional/services.html',
        services=services,
        form=form,
        delete_form=delete_form
    )


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


@professional.route('/services/<int:service_id>/delete', methods=['POST'])
@login_required
def delete_service(service_id):
    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        service = Service.query.get_or_404(service_id)
        if service.professional_id != current_user.id:
            abort(403)
        db.session.delete(service)
        db.session.commit()
        flash('Servicio eliminado exitosamente.', 'success')
    else:
        flash('Error en la eliminación. Intenta de nuevo.', 'danger')

    return redirect(url_for('professional.services'))

# -------------------------------------------------------
# PERFIL DEL PROFESIONAL
# -------------------------------------------------------

@professional.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        # Actualiza datos básicos
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.category = form.category.data
        current_user.subcategory = form.subcategory.data
        current_user.description = form.description.data
        current_user.experience = form.experience.data
        current_user.location = form.location.data
        current_user.website = form.website.data

        # 📎 Procesar archivo del certificado
        file = form.certificate_file.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            current_user.certificate_file = filename

        # 📸 Procesar imagen de perfil (opcional)
        image = form.profile_image.data
        if image:
            image_name = secure_filename(image.filename)
            image_path = os.path.join(app.root_path, 'static/uploads/profile_images', image_name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            current_user.profile_image = image_name

        db.session.commit()
        flash("Perfil actualizado correctamente.", "success")
        return redirect(url_for('professional.profile'))

    return render_template('professional/profile.html', form=form)


# Ruta para servir archivos subidos (certificados)
@professional.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# -------------------------------------------------------
# ACTIVAR PERFIL (POST-PAGO)
# -------------------------------------------------------

@professional.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        current_user.active = True
        db.session.commit()
        flash('Pago realizado. Tu perfil está activo.', 'success')
        return redirect(url_for('professional.dashboard'))
    return render_template('professional/payment.html')

# -------------------------------------------------------
# SOLICITUDES Y RESPUESTAS
# -------------------------------------------------------

@professional.route('/requests')
@login_required
def requests_list():
    solicitudes = (
        Request.query.join(Service)
        .filter(Service.professional_id == current_user.id)
        .order_by(Request.date_requested.desc())
        .all()
    )
    return render_template('professional/requests.html', solicitudes=solicitudes)


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


@professional.route('/requests/<int:request_id>/complete', methods=['POST'])
@login_required
def complete_request(request_id):
    req = Request.query.get_or_404(request_id)
    if req.service.professional_id != current_user.id:
        abort(403)

    if req.status == 'accepted':
        req.status = 'completed'
        db.session.commit()
        flash('Servicio marcado como completado.', 'success')
    else:
        flash('Solo servicios aceptados pueden completarse.', 'warning')

    return redirect(url_for('professional.requests_list'))

# -------------------------------------------------------
# HISTORIAL Y RESEÑAS
# -------------------------------------------------------

@professional.route('/history')
@login_required
def history():
    servicios = (
        Request.query.join(Service)
        .filter(Service.professional_id == current_user.id, Request.status == "completed")
        .order_by(Request.date_requested.desc())
        .all()
    )
    return render_template('professional/history.html', servicios=servicios)


@professional.route('/reviews')
@login_required
def reviews():
    evaluaciones = Evaluation.query.filter_by(professional_id=current_user.id).all()
    return render_template('professional/reviews.html', evaluaciones=evaluaciones)

# -------------------------------------------------------
# DISPONIBILIDAD HORARIA
# -------------------------------------------------------

@professional.route('/availability', methods=['GET', 'POST'])
@login_required
def availability():
    form = AvailabilityForm()
    delete_form = DeleteForm()

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
    return render_template(
        'professional/availability.html',
        form=form,
        disponibles=disponibles,
        delete_form=delete_form
    )


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
