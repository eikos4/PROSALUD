from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Service, User, Request, Message
from app.forms import ClientProfileForm, RequestServiceForm, MessageForm
from app import db
from app.forms import EvaluationForm
from app.models import Request, Evaluation
from app.models import Evaluation, User
from datetime import datetime

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



# Perfil del cliente FM.
from flask import flash, redirect, url_for
from app.models import User

@client.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ClientProfileForm(obj=current_user)

    if form.validate_on_submit():
        # Verificar que el username no esté tomado por otro usuario
        existing_user = User.query.filter(
            User.username == form.username.data,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            flash('Ese nombre de usuario ya está en uso. Por favor, elige otro.', 'danger')
            return redirect(url_for('client.profile'))

        # Guardar cambios
        current_user.username = form.username.data
        current_user.location = form.location.data
        db.session.commit()

        flash('Perfil actualizado correctamente', 'success')
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
    service = req.service
    if current_user.id == req.client_id:
        other_user = service.professional
    else:
        other_user = req.client

    convo = Message.get_conversation(current_user.id, other_user.id, service.id)
    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            receiver_id=other_user.id,
            service_id=service.id,
            body=form.body.data.strip()
        )
        db.session.add(msg)
        db.session.commit()
        flash("Mensaje enviado", "success")
        return redirect(url_for('client.request_detail', request_id=req.id))

    return render_template(
        'client/request_detail.html',
        req=req,
        other_user=other_user,
        convo=convo,
        form=form,
    )


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





@client.route('/add_review/<int:user_id>', methods=['POST'])
@login_required
def add_review(user_id):
    """Permite al cliente dejar una reseña directa en el perfil de un profesional."""
    professional = User.query.get_or_404(user_id)

    rating = int(request.form.get('rating', 0))
    comment = request.form.get('comment', '').strip()

    if not rating or not comment:
        flash('Por favor, completa la calificación y el comentario.', 'warning')
        return redirect(url_for('main.public_profile', id=user_id))

    # Evita duplicar reseñas del mismo cliente al mismo profesional
    existing_review = Evaluation.query.filter_by(client_id=current_user.id, professional_id=user_id).first()
    if existing_review:
        flash('Ya has dejado una reseña para este profesional.', 'info')
        return redirect(url_for('main.public_profile', id=user_id))

    new_review = Evaluation(
        professional_id=professional.id,
        client_id=current_user.id,
        rating=rating,
        comment=comment,
        created_at=datetime.utcnow()
    )

    db.session.add(new_review)
    db.session.commit()
    flash('¡Tu reseña fue enviada correctamente!', 'success')
    return redirect(url_for('main.public_profile', id=user_id))

