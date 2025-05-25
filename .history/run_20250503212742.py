# run.py

from app import create_app, db

app = create_app()

# ★ Solo durante desarrollo ★
if __name__ == '__main__':
    with app.app_context():
          # Crea las tablas que falten
    app.run(debug=True)
