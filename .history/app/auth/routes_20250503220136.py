from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
from app.models import User
from app.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

# app/auth/routes.py

from app.models import User
from sqlalchemy.exc import IntegrityError


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data  # ← aquí asignas el rol
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    # Si hay errores de validación, los mostramos
    if request.method == 'POST':
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{getattr(form, field).label.text}: {err}", 'danger')

    return render_template('auth/register.html', form=form)

# app/auth/routes.py
@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if usuario.role == 'professional':
            if user.role == 'professional':
                flash('Redirigiendo al dashboard Profesional', 'info')
                return redirect(url_for('professional.dashboard'))
            else:
-               flash('Redirigiendo al dashboard Cliente', 'info')
+               flash('Redirigiendo al dashboard Cliente', 'info')
                return redirect(url_for('client.dashboard'))
        flash('Email o contraseña incorrectos', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
