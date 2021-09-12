from functools import wraps
from flask import session, request, redirect, url_for
from flask.helpers import flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("You must be logged in to access", "bg-red-400")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function