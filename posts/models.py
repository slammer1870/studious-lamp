from flask import Flask, jsonify, request, session, redirect, url_for
import uuid
from datetime import datetime
from app import db



class Post:
    def create(self, form):
        post = {
        "_id": uuid.uuid4().hex,
        "owner": session['user'],
        "date": datetime.now(),
        "post": form.post.data
        }

        db.posts.insert_one(post)
        return True

    def edit(self, id, form):
        db.posts.find_one_and_update({"_id": id}, {"$set": {"post": form.post.data}})
        return True

    def delete(self, id):
        db.posts.delete_one({"_id": id})
        return True




