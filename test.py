# create_test_user.py

from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Borra usuarios previos con este email, si lo deseas:
    User.query.filter_by(email='fabricio_test@example.com').delete()
    # Crea el nuevo
    u = User(username='Fabricio', email='fabricio_test@example.com')
    u.set_password('Secret123')
    u.is_active = True
    db.session.add(u)
    db.session.commit()
    print(f'Usuario creado: {u.username} (ID={u.id})')

