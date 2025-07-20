# create_100_simpsons_users.py

from app import create_app, db
from app.models import User
import random
import unicodedata

# Lista de nombres completos de personajes de Los Simpsons
simpsons_full_names = [
    'Homero Simpson', 'Marge Simpson', 'Bart Simpson', 'Lisa Simpson', 'Maggie Simpson',
    'Ned Flanders', 'Milhouse Van Houten', 'Nelson Muntz', 'Ralph Wiggum', 'Seymour Skinner',
    'Montgomery Burns', 'Waylon Smithers', 'Apu Nahasapeemapetilon', 'Barney Gumble', 'Lenny Leonard',
    'Carl Carlson', 'Moe Szyslak', 'Otto Mann', 'Patty Bouvier', 'Selma Bouvier', 'Edna Krabappel',
    'Krusty El Payaso', 'Martin Prince', 'Willie El Jardinero', 'Clancy Wiggum', 'Troy McClure',
    'Todd Flanders', 'Rod Flanders', 'Luann Van Houten', 'Kirk Van Houten', 'Agnes Skinner',
    'Helen Lovejoy', 'Reverendo Lovejoy', 'Snake Jailbird', 'Jasper Beardly', 'Üter Zörker',
    'Gil Gunderson', 'Allison Taylor', 'Shauna Chalmers', 'Julius Hibbert'
]

# Función para generar usernames válidos
def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text.lower().replace(' ', '_')

app = create_app()

with app.app_context():
    # Borrar usuarios anteriores creados para prueba (si existen)
    User.query.filter(User.email.like('simpson%@prosalud.cl')).delete(synchronize_session=False)
    db.session.commit()

    for i in range(100):
        nombre_completo = random.choice(simpsons_full_names)
        email = f"simpson{i}@prosalud.cl"
        username = f"{slugify(nombre_completo)}_{i}"

        user = User(
            username=username,
            email=email,
            role='professional',
            is_active=True
        )
        user.set_password('Secret123')
        db.session.add(user)

    db.session.commit()
    print("✅ Se crearon 100 profesionales tipo Simpsons.")
