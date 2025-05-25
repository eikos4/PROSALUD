from flask import render_template, redirect, url_for
from app import app



@app.route('/login')
def login():
    return render_template('/login.html')
