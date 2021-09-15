from wtforms import Form, StringField, validators
from wtforms.fields.html5 import EmailField
class NewsletterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=6, max=50), validators.DataRequired(), validators.Email()])
