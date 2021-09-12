from flask import Flask, render_template, session, g, request, redirect, url_for
import os
import pymongo
from werkzeug.utils import redirect
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.widgets import TextArea
import uuid
from datetime import datetime
from wraps import login_required

app = Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY")

# Database
client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
db = client.flaskDB

# Routes
from auth import forms, routes
from posts import routes


@app.route("/")
def index():
	return render_template("index.html")

# Register Form Class
class PostForm(Form):
    post = TextAreaField('Post', [validators.Length(min=1, max=180)])

@app.route("/dashboard/", methods=['GET', 'POST'])
@login_required
def dashboard():
    posts = db.posts.find()
    yours = db.posts.find({"owner": session['user']})
    form = PostForm(request.form)
    if posts != 0:
        return render_template("dashboard.html", posts=posts, form=form, yours=yours)
    return render_template("dashboard.html", form=form)

if __name__ == '__main__':
	app.run(debug=True)

class NewsletterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])

