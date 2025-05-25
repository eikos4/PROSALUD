from flask import Blueprint, render_template, request
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/search')
def search():
    q = request.args.get('q', '')
    # Busca en el campo 'description' de User
    results = User.query.filter(
        User.description.ilike(f'%{q}%')
    ).all()
    return render_template('main/search.html', query=q, results=results)
