# validate_pro_user.py
import argparse
from datetime import datetime

from app import create_app, db
from app.models import User

FIELDS_TRUE = [
    "is_professional",        # bool: indica que es cuenta profesional
    "is_pro_verified",        # bool: verificación de credenciales/pago
    "pro_payment_confirmed",  # bool: pago validado
    "active_pro",             # bool: estado pro activo
    "is_active",              # bool: acceso general
]
FIELDS_STATUS = {
    "pro_status": "active",           # enum/str: 'pending' -> 'active'
    "verification_status": "verified" # enum/str
}
FIELDS_TIMESTAMP = [
    "pro_verified_at",       # datetime
    "verified_at",           # datetime
    "pro_activated_at",      # datetime
]

def activate_user(u: User) -> list[str]:
    changes = []

    # Forzar profesional activo
    for f in FIELDS_TRUE:
        if hasattr(u, f):
            setattr(u, f, True)
            changes.append(f"{f}=True")

    # Estados en texto
    for f, val in FIELDS_STATUS.items():
        if hasattr(u, f):
            setattr(u, f, val)
            changes.append(f"{f}='{val}'")

    # Timestamps
    now = datetime.utcnow()
    for f in FIELDS_TIMESTAMP:
        if hasattr(u, f):
            setattr(u, f, now)
            changes.append(f"{f}={now.isoformat()}Z")

    return changes

def main():
    parser = argparse.ArgumentParser(description="Activar/validar cuenta profesional.")
    parser.add_argument("--email", required=True, help="Email del usuario a activar")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        u = User.query.filter_by(email=args.email).first()
        if not u:
            print(f"[ERROR] No se encontró usuario con email: {args.email}")
            return

        changes = activate_user(u)
        db.session.commit()
        print(f"[OK] Usuario {u.username} ({u.email}) activado/validado.")
        if changes:
            print("Cambios aplicados:")
            for c in changes:
                print("  -", c)
        else:
            print("No se detectaron campos típicos para activar PRO. Revisa el modelo User.")

if __name__ == "__main__":
    main()
