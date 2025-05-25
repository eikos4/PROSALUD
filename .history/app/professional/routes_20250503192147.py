from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import ProfileForm
from app.models import User

professional = Blueprint('professional', __name__, url_prefix='/professional')

@professional.route('/dashboard')
@login_required
def dashboard():
    return render_template('professional/dashboard.html')

@professional.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Perfil actualizado.', 'success')
        return redirect(url_for('professional.dashboard'))
    return render_template('professional/profile.html', form=form)

# app/professional/routes.py

@professional.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        # Aquí marcas al usuario como activo
        current_user.active = True    # usa el campo booleano 'active'
        db.session.commit()           # guarda el cambio en la DB
        flash('Pago realizado. Tu perfil está activo.', 'success')
        return redirect(url_for('professional.dashboard'))
    return render_template('professional/payment.html')


@professional.route('/professional/dashboard')
@login_required
def dashboard():
    # tu lógica...
    return render_template('professional/dashboard.html')
