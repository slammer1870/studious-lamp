from flask import Flask, render_template, session, g, request, redirect, url_for, flash
import os
import pymongo
from werkzeug.utils import redirect
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField
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
db = client[str(os.environ.get("DB_NAME"))]

# Routes
from auth import forms, routes
from posts import routes
from newsletter import routes
from newsletter.forms import NewsletterForm

# Contact Form Class 
class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
    message = TextAreaField('Message', [validators.Length(min=1, max=180), validators.DataRequired()])

@app.route("/")
def index():
    form = NewsletterForm(request.form)
    contact = ContactForm(request.form)
    return render_template("index.html", form=form, contact=contact)


#Route to handle contact from submission using the sendgrid API
@app.route("/contact/", methods=['POST'])
def contact():
    news = NewsletterForm(request.form)
    form = ContactForm(request.form)        
    if request.method == 'POST' and form.validate(): #Check form post data is valid
        message = Mail(
            from_email='hello@sammcnally.dev',
            to_emails='hello@sammcnally.dev',
            subject='New form submission from {}'.format(form.name.data),
            plain_text_content=form.message.data)
        message.reply_to=form.email.data, form.name.data
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY')) #Initialises Sendgrid Client
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
    return render_template("index.html", form=news, contact=form)


# Post Form Class
class PostForm(Form):
    post = TextAreaField('Post', [validators.DataRequired(), validators.Length(min=1, max=180)])

@app.route("/dashboard/", methods=['GET', 'POST'])
#Login required decorator
@login_required
def dashboard():
    posts = db.posts.find()
    yours = db.posts.find({"owner": session['user']})
    form = PostForm(request.form)
    return render_template("dashboard.html", posts=posts, form=form, yours=yours)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(debug=True)

