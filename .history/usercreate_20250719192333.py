# create_test_users.py

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Opcional: eliminar usuarios anteriores con estos correos
    User.query.filter(User.email.in_([
        'pro_test@example.com',
        'cliente_test@example.com'
    ])).delete(synchronize_session=False)

    # Crear Profesional
    profesional = User(
        username='',
        email='pro_test@example.com',
        role='professional',
        is_active=True
    )
    profesional.set_password('Secret123')

    # Crear Cliente
    cliente = User(
        username='Homero Simsonson',
        email='cliente_test@example.com',
        role='client',
        is_active=True
    )
    cliente.set_password('Secret123')

    # Guardar en la BD
    db.session.add_all([profesional, cliente])
    db.session.commit()

    print(f"Profesional creado: {profesional.username} (ID={profesional.id})")
    print(f"Cliente creado: {cliente.username} (ID={cliente.id})")
