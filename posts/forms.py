from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# Register Form Class
class PostForm(Form):
    post = TextAreaField('Post', [validators.required(), validators.length(min=4, max=200)])