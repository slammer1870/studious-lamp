from flask import Flask, session
import uuid
from datetime import datetime
from app import db

class Post:

    #Post create method
    def create(self, form):
        post = {
        "_id": uuid.uuid4().hex,
        "owner": session['user'], #ForeignKey to User
        "date": datetime.now(),
        "post": form.post.data
        }

        db.posts.insert_one(post)
        return True

    #Post edit method
    def edit(self, id, form):
        db.posts.find_one_and_update({"_id": id}, {"$set": {"post": form.post.data}})
        return True

    #Post delete method
    def delete(self, id):
        db.posts.delete_one({"_id": id})
        return True




