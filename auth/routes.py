from flask import Flask, render_template, request
from __main__ import app
from flask.helpers import url_for

from pymongo.common import validate
from werkzeug.utils import redirect
from auth.models import User
from .forms import RegisterForm, LogInForm

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        if user.register(form):
            return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LogInForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        if user.login(form):
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    user = User()
    return user.logout()
