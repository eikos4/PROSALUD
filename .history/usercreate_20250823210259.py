from datetime import datetime
from app import db
from app.models import User

email = "swap.1319@gmail.com"
u = User.query.filter_by(email=email).first()
if not u:
    print("No existe."); 
else:
    for f in ["is_professional","is_pro_verified","pro_payment_confirmed","active_pro","is_active"]:
        if hasattr(u, f): setattr(u, f, True)
    if hasattr(u, "pro_status"): u.pro_status = "active"
    if hasattr(u, "verification_status"): u.verification_status = "verified"
    now = datetime.utcnow()
    for f in ["pro_verified_at","verified_at","pro_activated_at"]:
        if hasattr(u, f): setattr(u, f, now)
    db.session.commit()
    print("OK activado:", u.email)
