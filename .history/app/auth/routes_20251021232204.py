from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm, UpgradeAccountForm
from urllib.parse import urlparse, urljoin

auth = Blueprint('auth', __name__)

def is_safe_url(target):
    ref_url  = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Validar que el username NO esté ya registrado
        if User.query.filter_by(username=form.username.data).first():
            flash("El nombre de usuario ya está registrado. Usa otro.", "danger")
            return render_template('auth/register.html', form=form)
        # Validar que el email NO esté ya registrado
        if User.query.filter_by(email=form.email.data).first():
            flash("Ya existe una cuenta registrada con ese email.", "danger")
            return render_template('auth/register.html', form=form)
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:  # Fallback por si acaso
            db.session.rollback()
            flash('Ya existe un usuario con ese nombre o email.', 'danger')
            return render_template('auth/register.html', form=form)

    # Mostrar errores de validación del formulario
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

            # 🔹 Solo mostrar advertencia, sin bloquear
            if user.role == 'professional' and not user.active:
                flash('Tu cuenta profesional aún no está activa. Revisa tu correo o envía tu CV para confirmar.', 'warning')

            login_user(user, remember=form.remember_me.data)
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')

            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)

            # Redirige según el rol
            if user.role == 'professional':
                return redirect(url_for('professional.dashboard'))
            return redirect(url_for('client.dashboard'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))


@auth.route("/terms")
def terms():
    return render_template("terms.html")

@auth.route("/privacy")
def privacy():
    return render_template("privacy.html")
