from flask import render_template, redirect, url_for
from app import app

@app.route('/')
def home():
    return render_template('main/index.html')

@app.route('/login')
def login():
    return render_template('main/login.html')
