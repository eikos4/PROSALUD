# create_test_user.py

from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Borra usuarios previos con este email, si lo deseas:
    User.query.filter_by(email='pro_test@example.com').delete()
    # Crea el nuevo
    u = User(username='pro_test', email='pro_test@example.com')
    u.set_password('Secret123')
    u.is_active = True
    db.session.add(u)
    db.session.commit()
    print(f'Usuario creado: {u.username} (ID={u.id})')





from app import db
from app.models import User

# Busca tu usuario por email (reemplaza por tu email real)
user = User.query.filter_by(email='correo@demo.com').first()

# Cambia el campo active a True
user.active = True

# Guarda los cambios
db.session.commit()

# (Opcional) Verifica que quedó activo:
print(user.active)  # Debe decir True
