from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# Register Form Class
class LogInForm(Form):
    email = EmailField('Email', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])
