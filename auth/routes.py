from flask import Flask, render_template, request
from __main__ import app
from flask.helpers import url_for

from pymongo.common import validate
from werkzeug.utils import redirect
from auth.models import User
from .forms import RegisterForm

@app.route('/register', methods=['POST', 'GET'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        if user.register(form):
            return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)
