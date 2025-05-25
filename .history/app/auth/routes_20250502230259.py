from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
from app.models import User
from app.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

# app/auth/routes.py

from app.models import User
from sqlalchemy.exc import IntegrityError

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 1) Verifica duplicados
        if User.query.filter_by(username=form.username.data).first():
            flash('El nombre de usuario ya está en uso.', 'danger')
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('El correo ya está registrado.', 'danger')
            return render_template('auth/register.html', form=form)

        # 2) Crea normalmente
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.is_active = 
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Ocurrió un error al crear el usuario. Intenta con otro nombre o correo.', 'danger')
            return render_template('auth/register.html', form=form)

        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    # Si falló validación de WTForms, mostrá errores
    if request.method == 'POST':
        for field, errs in form.errors.items():
            for err in errs:
                flash(f"{getattr(form, field).label.text}: {err}", 'danger')

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Email o contraseña incorrectos', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
