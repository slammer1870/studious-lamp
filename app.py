from flask import Flask, render_template, session, g, request, redirect, url_for, flash
import os
import pymongo
from werkzeug.utils import redirect
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.widgets import TextArea
import uuid
from datetime import datetime
from wraps import login_required
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY")

# Database
client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
db = client.flaskDB

# Routes
from auth import forms, routes
from posts import routes
from newsletter import routes
from newsletter.forms import NewsletterForm

# Contact Form Class
class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    message = TextAreaField('Message', [validators.Length(min=1, max=180)])

@app.route("/")
def index():
    form = NewsletterForm(request.form)
    contact = ContactForm(request.form)
    return render_template("index.html", form=form, contact=contact)


#Route to handle contact from submission using the sendgrid API
@app.route("/contact/", methods=['POST'])
def contact():
    form = ContactForm(request.form)        
    if request.method == 'POST' and form.validate():
        message = Mail(
            from_email='hello@sammcnally.dev',
            to_emails='hello@sammcnally.dev',
            subject='New form submission from {}'.format(form.name.data),
            plain_text_content=form.message.data)
        message.reply_to=form.email.data, form.name.data
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            flash("Thank you for your message, we will respond shortly", "bg-green-400")
            return redirect(url_for('index'))
        except Exception as e:
            print(e.message)
            flash("Oops something went wrong", "bg-red-400")
            return redirect(url_for('index'))
    flash("Oops something went wrong", "bg-red-400")
    return redirect(url_for('index'))


# Post Form Class
class PostForm(Form):
    post = TextAreaField('Post', [validators.Length(min=1, max=180)])

@app.route("/dashboard/", methods=['GET', 'POST'])
#Login required decorator
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

