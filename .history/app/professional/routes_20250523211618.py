from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import ProfileForm
from app.models import User

professional = Blueprint('professional', __name__, url_prefix='/professional')

@professional.route('/dashboard')
@login_required
def dashboard():
    # Aquí podrías pasar datos extra al dashboard
    return render_template('professional/dashboard.html')

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

@professional.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        current_user.active = True
        db.session.commit()
        flash('Pago realizado. Tu perfil está activo.', 'success')
        return redirect(url_for('professional.dashboard'))
    return render_template('professional/payment.html')



from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Service, Request, Evaluation, Availability
from app.forms import ServiceForm, AvailabilityForm, ResponseRequestForm

professional = Blueprint('professional', __name__, url_prefix='/professional')

# === 1. Ver y gestionar solicitudes recibidas ===
@professional.route('/requests')
@login_required
def requests_list():
    solicitudes = Request.query\
        .join(Service)\
        .filter(Service.professional_id == current_user.id)\
        .order_by(Request.date_requested.desc()).all()
    return render_template('professional/requests.html', solicitudes=solicitudes)

# === 2. Aceptar o rechazar solicitud ===
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

# === 3. Ver historial de servicios prestados ===
@professional.route('/history')
@login_required
def history():
    servicios = Request.query\
        .join(Service)\
        .filter(Service.professional_id == current_user.id, Request.status == "completed")\
        .order_by(Request.date_requested.desc()).all()
    return render_template('professional/history.html', servicios=servicios)

# === 4. Ver evaluaciones recibidas ===
@professional.route('/reviews')
@login_required
def reviews():
    evaluaciones = Evaluation.query.filter_by(professional_id=current_user.id).all()
    return render_template('professional/reviews.html', evaluaciones=evaluaciones)

# === 5. Configurar disponibilidad ===
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
