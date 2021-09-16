from wtforms import Form, TextAreaField, validators


# Register Form Class
class PostForm(Form):
    post = TextAreaField('Post', [validators.required(), validators.Length(min=4, max=180, message='Post cannot be longer than 180 characters')])