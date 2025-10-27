from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User
from app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')


# --- Validación de permisos (solo administradores) ---
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Acceso denegado. Solo administradores pueden entrar aquí.", "danger")
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return wrapper


# --- Dashboard principal del admin ---
@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    professionals = User.query.filter_by(role='professional').order_by(User.active.desc()).all()
    return render_template('admin/dashboard.html', professionals=professionals)


# --- Aprobar o desactivar un profesional ---
@admin.route('/toggle/<int:user_id>')
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'professional':
        flash("Solo se pueden modificar cuentas profesionales.", "warning")
        return redirect(url_for('admin.dashboard'))

    user.active = not user.active
    db.session.commit()

    if user.active:
        flash(f"✅ {user.username} ha sido aprobado y ahora aparece en la plataforma.", "success")
    else:
        flash(f"⚠️ {user.username} ha sido desactivado.", "info")

    return redirect(url_for('admin.dashboard'))
