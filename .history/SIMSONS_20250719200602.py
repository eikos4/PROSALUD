from app import create_app, db
from app.models import User
import random

# Lista base de nombres y apellidos (puedes ampliarla si lo deseas)
simpsons_names = [
    'Homero Simpson',
    'Marge Simpson',
    'Bart Simpson',
    'Lisa Simpson',
    'Maggie Simpson',
    'Ned Flanders',
    'Milhouse Van Houten',
    'Nelson Muntz',
    'Ralph Wiggum',
    'Seymour Skinner',
    'Montgomery Burns',
    'Waylon Smithers',
    'Apu Nahasapeemapetilon',
    'Barney Gumble',
    'Lenny Leonard',
    'Carl Carlson',
    'Moe Szyslak',
    'Otto Mann',
    'Patty Bouvier',
    'Selma Bouvier',
    'Edna Krabappel',
    'Krusty El Payaso',
    'Martin Prince',
    'Willie El Jardinero',
    'Clancy Wiggum',
    'Troy McClure',
    'Todd Flanders',
    'Rod Flanders',
    'Luann Van Houten',
    'Kirk Van Houten',
    'Agnes Skinner',
    'Helen Lovejoy',
    'Reverendo Lovejoy',
    'Snake Jailbird',
    'Jasper Beardly',
    'Üter Zörker',
    'Gil Gunderson',
    'Allison Taylor',
    'Shauna Chalmers',
    'Julius Hibbert'
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
