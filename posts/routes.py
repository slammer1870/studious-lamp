from flask import Flask, request, session
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from posts.forms import PostForm
from app import app
from .models import Post
from .forms import PostForm
from app import db

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

@app.route('/posts/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    form = PostForm(request.form)
    post = db.posts.find_one({"_id": id})
    form.post.data = post['post']
    if request.method == "POST" and form.validate():
        post = Post()
        new_form = PostForm(request.form)
        post.edit(id, new_form)
        flash("Post has been updated", "bg-yellow-400")
        return redirect(url_for('dashboard'))
    return render_template("edit_post.html", form=form)

@app.route('/posts/delete/<string:id>', methods=['POST'])
def delete(id):
    post = Post()
    post.delete(id)
    flash("Post has been deleted", "bg-yellow-400")
    return redirect(url_for('dashboard'))
