from flask import Flask, render_template, session
import os
from flask.globals import request
from flask.helpers import url_for
import pymongo
from werkzeug.utils import redirect
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.widgets import TextArea
import uuid
from datetime import datetime

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
def dashboard():
    posts = db.posts.find()
    form = PostForm(request.form)
    if posts != 0:
        return render_template("dashboard.html", posts=posts, form=form)
    return render_template("dashboard.html", form=form)

if __name__ == '__main__':
	app.run(debug=True)