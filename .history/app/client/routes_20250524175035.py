from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import User

from app.forms import ClientProfileForm

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Service, User, Request
from app.forms import RequestServiceForm

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/dashboard')
@login_required
def dashboard():
    # Parámetros de búsqueda y filtro
    q      = request.args.get('q', '').strip()
    region = request.args.get('region', '').strip()

    # Consulta base: solo profesionales activos
    query = User.query.filter_by(role='professional', active=True)

    if q:
        query = query.filter(User.username.ilike(f'%{q}%'))
    if region:
        query = query.filter(User.location == region)

    professionals = query.all()

    # Obtener lista única de regiones
    regions = sorted({
        u.location for u in User.query.with_entities(User.location).distinct() 
        if u.location
    })

    return render_template(
        'client/dashboard.html',
        professionals=professionals,
        regions=regions,
        selected_region=region,
        search_term=q
    )


@client.route('/request_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def request_service(service_id):
    service = Service.query.get_or_404(service_id)
    professional = User.query.get(service.professional_id)
    form = RequestServiceForm()
    if form.validate_on_submit():
        req = Request(
            client_id=current_user.id,
            service_id=service.id,
            message=form.message.data.strip()
        )
        db.session.add(req)
        db.session.commit()
        flash('Solicitud enviada correctamente.', 'success')
        return redirect(url_for('client.my_requests'))  # O donde quieras redirigir
    return render_template('client/request_service.html', form=form, service=service, professional=professional)



@client.route('/my_requests')
@login_required
def my_requests():
    # Aquí asumes que tienes un modelo Request
    solicitudes = Request.query.filter_by(client_id=current_user.id).order_by(Request.date_requested.desc()).all()
    return render_template('client/my_requests.html', solicitudes=solicitudes)



@client.route('/history')
@login_required
def history():
    # Busca las solicitudes/compras completadas por el cliente
    servicios = Request.query.filter_by(client_id=current_user.id, status='completed').order_by(Request.date_requested.desc()).all()
    return render_template('client/history.html', servicios=servicios)



@client.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ClientProfileForm(obj=current_user)  # Usa tu form adecuado
    if form.validate_on_submit():
        # Actualiza los datos del cliente (ajusta campos según tu modelo)
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('client.profile'))
    return render_template('client/profile.html', form=form)
