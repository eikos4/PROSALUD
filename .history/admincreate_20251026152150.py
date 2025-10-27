# create_admin.py
"""
Script para crear un usuario administrador en PROSALUD.
Ejecutar con:  python create_admin.py
"""

from app import create_app, db
from app.models import User

def create_admin():
    """Crea un usuario administrador en la base de datos."""
    app = create_app()

    with app.app_context():
        # Datos del administrador
        email = "admin@prosalud.cl"
        username = "admin"
        password = "admin123"  # ⚠️ cámbiala después por seguridad
        role = "admin"

        # Verificar si ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"⚠️ Ya existe un usuario con el correo: {email}")
            return

        # Crear nuevo usuario admin
        admin = User(
            username=username,
            email=email,
            role=role,
            active=True  # Los administradores siempre están activos
        )
        admin.set_password(password)

        # Guardar en la base de datos
        db.session.add(admin)
        db.session.commit()

        print("✅ Usuario administrador creado correctamente:")
        print(f"👤 Usuario: {username}")
        print(f"📧 Email: {email}")
        print(f"🔑 Contraseña: {password}")
        print(f"🎩 Rol: {role}")

if __name__ == "__main__":
    create_admin()
