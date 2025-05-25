from flask import Blueprint, render_template, request
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

from sqlalchemy import or_

@main.route('/search')
def search():
    q = request.args.get('q', '')
    results = User.query.filter(
        or_(
            User.username.ilike(f'%{q}%'),
            User.category.ilike(f'%{q}%'),
            User.description.ilike(f'%{q}%')
        )
    ).all()
    return render_template('main/search.html', query=q, results=results)
