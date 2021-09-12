from flask import Flask, request, session
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from posts.forms import PostForm
from app import app
from .models import Post
from .forms import PostForm
import uuid
from datetime import datetime

@app.route('/posts/create/', methods=['POST'])
def create():
    form = PostForm(request.form)
    if request.method == "POST" and form.validate():
        post = Post()
        post.create(form)
        flash("New post has been created", "bg-yellow-400")
        return redirect(url_for('dashboard'))
    flash("An error occured, post not created", "bg-red-400")
    return redirect(url_for('dashboard'))
