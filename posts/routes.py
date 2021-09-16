from flask import Flask, request, session
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from posts.forms import PostForm
from app import app
from .models import Post
from .forms import PostForm
from app import db
from wraps import login_required


#Post create endpoint
@app.route('/posts/create/', methods=['POST'])
@login_required
def create():
    form = PostForm(request.form)
    if request.method == "POST" and form.validate(): #Checks that from posts valid data
        post = Post()
        post.create(form)
        flash("New post has been created", "bg-yellow-400")
        return redirect(url_for('dashboard'))
    flash("An error occured, post not created", "bg-red-400")
    #Template rendered with calls to database only if post request is invalid
    return render_template("dashboard.html", form=form, posts=db.posts.find(), yours=db.posts.find({"owner": session['user']})
)


@app.route('/posts/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = PostForm(request.form)
    post = db.posts.find_one({"_id": id})
    if post :
        if session['user']['_id'] == post['owner']['_id']: #Check that current logged in user is the post owner
            form.post.data = post['post']
            if request.method == "POST" and form.validate():
                post = Post()
                new_form = PostForm(request.form)
                post.edit(id, new_form)
                flash("Post has been updated", "bg-yellow-400")
                return redirect(url_for('dashboard'))
            return render_template("edit_post.html", form=form)
    flash("Permission denied, you must be the owner of this post to edit", "bg-yellow-400")
    return redirect(url_for('dashboard'))

@app.route('/posts/delete/<string:id>', methods=['POST'])
@login_required
def delete(id):
    post = db.posts.find_one({"_id": id})
    if post :
        if session['user']['_id'] == post['owner']['_id']: #Check that current logged in user is the post owner
            post = Post()
            post.delete(id)
            flash("Post has been deleted", "bg-yellow-400")
            return redirect(url_for('dashboard'))
    flash("Permission denied, you must be the owner of this post to delete", "bg-yellow-400")
    return redirect(url_for('dashboard'))
