from flask import Flask, jsonify, request, session, redirect, url_for
import uuid
from datetime import datetime
from app import db


class Post:
    def create(self, form):
        print(request)
        post = {
        "_id": uuid.uuid4().hex,
        "owner": session['user'],
        "date": datetime.now(),
        "post": form.post.data
        }

        db.posts.insert_one(post)
