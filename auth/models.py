  
from flask import Flask, jsonify, request, session, redirect, url_for
from flask.helpers import flash
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

#Define User class

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return 200

    #User object register method
    def register(self, form):

        # Create the user object
        user = {
        "_id": uuid.uuid4().hex,
        "name": form.name.data,
        "email": form.email.data,
        "password": form.password.data
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(form.password.data)

        # Check for existing email address
        if db.users.find_one({ "email": user['email'] }):
            flash("User already exists", "bg-red-400")
            return False

        if db.users.insert_one(user):
            self.start_session(user)
            flash("Thank you for registering, you are now logged in!", "bg-green-400")
            return True

    def login(self, form):

        user = db.users.find_one({
        "email": form.get('email')
        })

        if user and pbkdf2_sha256.verify(form.get('password'), user['password']):
            self.start_session(user)
            flash("Thank you for registering, you are now logged in!", "bg-green-400")
            return True
        
        return flash("Invalid login credentials", "bg-red-400")