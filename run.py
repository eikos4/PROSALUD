# run.py

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # ★ Solo durante desarrollo ★
    with app.app_context():
        # Crea aquí únicamente las tablas que falten (no recrea las ya existentes)
        db.create_all()
    app.run(debug=True)
