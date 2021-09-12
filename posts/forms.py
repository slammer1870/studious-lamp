from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# Register Form Class
class PostForm(Form):
    post = TextAreaField('Post', [validators.optional(), validators.length(max=200)])