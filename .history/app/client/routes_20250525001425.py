from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Service, User, Request, Message
from app.forms import ClientProfileForm, RequestServiceForm, MessageForm
from app import db

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/dashboard')
@login_required
def dashboard():
    q      = request.args.get('q', '').strip()
    region = request.args.get('region', '').strip()
    query = User.query.filter_by(role='professional', active=True)
    if q:
        query = query.filter(User.username.ilike(f'%{q}%'))
    if region:
        query = query.filter(User.location == region)
    professionals = query.all()
    regions = sorted({
        u.location for u in User.query.with_entities(User.location).distinct() if u.location
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
        return redirect(url_for('client.my_requests'))
    return render_template('client/request_service.html', form=form, service=service, professional=professional)

@client.route('/history')
@login_required
def history():
    servicios = Request.query.filter_by(client_id=current_user.id, status='completed').order_by(Request.date_requested.desc()).all()
    return render_template('client/history.html', servicios=servicios)

@client.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ClientProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('client.profile'))
    return render_template('client/profile.html', form=form)

@client.route('/my_requests')
@login_required
def my_requests():
    requests = Request.query.filter_by(client_id=current_user.id).all()
    return render_template('client/my_requests.html', requests=requests)

@client.route('/my_requests/<int:request_id>', methods=['GET', 'POST'])
@login_required
def request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    messages = []  # si no hay modelo Message relacionado, deja vacío
    form = MessageForm()
    return render_template(
        'client/request_detail.html',
        req=req,
        messages=messages,
        form=form
    )

from app.forms import EvaluationForm
from app.models import Request, Evaluation

@client.route('/evaluate/<int:request_id>', methods=['GET', 'POST'])
@login_required
def evaluate(request_id):
    req = Request.query.get_or_404(request_id)
    # Seguridad: solo cliente creador y solo si está completed
    if req.client_id != current_user.id or req.status != 'completed':
        abort(403)
    # Verifica que no haya evaluación previa
    if Evaluation.query.filter_by(client_id=current_user.id, professional_id=req.service.professional.id, request_id=req.id).first():
        flash("Ya evaluaste este servicio.", "info")
        return redirect(url_for('client.my_requests'))
    form = EvaluationForm()
    if form.validate_on_submit():
        eval = Evaluation(
            professional_id=req.service.professional.id,
            client_id=current_user.id,
            rating=form.rating.data,
            comment=form.comment.data,
            request_id=req.id
        )
        db.session.add(eval)
        db.session.commit()
        flash('¡Reseña enviada!', 'success')
        return redirect(url_for('client.my_requests'))  # O al detalle de la solicitud si prefieres
    return render_template('client/evaluate.html', form=form, req=req)
