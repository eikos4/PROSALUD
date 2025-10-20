
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Busca tu usuario por email
    user = User.query.filter_by(email='felipe_pro@example.com').first()
    
    if user:
        # ✅ CORRECCIÓN: Usar is_active en lugar de active
        user.is_active = True
        
        # Guarda los cambios
        db.session.commit()
        
        # Verifica que quedó activo
        print(f"Usuario {user.username} activado: {user.is_active}")
    else:
        print("Usuario no encontrado")
