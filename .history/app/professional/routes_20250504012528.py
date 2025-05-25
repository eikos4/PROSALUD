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
