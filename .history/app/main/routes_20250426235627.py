from flask import Blueprint, render_template, request
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

