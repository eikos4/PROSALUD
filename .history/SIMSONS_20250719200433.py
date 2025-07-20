from app import create_app, db
from app.models import User
import random

# Lista base de nombres y apellidos (puedes ampliarla si lo deseas)
simpsons_names = [
    'Homero', 'Marge', 'Bart', 'Lisa', 'Maggie', 'Flanders', 'Milhouse', 'Nelson',
    'Ralph', 'Skinner', 'Burns', 'Smithers', 'Apu', 'Barney', 'Lenny', 'Carl',
    'Moe', 'Otto', 'Patty', 'Selma', 'Edna', 'Krusty', 'Martin', 'Willie',
    'Wiggum', 'Troy', 'Todd', 'Rod', 'Luann', 'Kirk', 'Agnes', 'Helen',
    'Lovejoy', 'Snake', 'Jasper', 'Uter', 'Gil', 'Allison', 'Shauna', 'Hibbert'
]

app = create_app()

with app.app_context():
    # Eliminar previamente los usuarios de prueba, si existen
    User.query.filter(User.email.like('simpson%@prosalud.cl')).delete(synchronize_session=False)
    db.session.commit()

    for i in range(100):
        nombre = random.choice(simpsons_names)
        apellido = random.choice(simpsons_names)
        full_name = f"{nombre} {apellido}"
        email = f"simpson{i}@prosalud.cl"
        username = f"{nombre.lower()}_{apellido.lower()}_{i}"

        user = User(
            username=username,
            full_name=full_name,
            email=email,
            role='professional',
            is_active=True
        )
        user.set_password('Secret123')
        db.session.add(user)

    db.session.commit()
    print("✅ Se crearon 100 profesionales de prueba con nombres tipo Simpsons.")
