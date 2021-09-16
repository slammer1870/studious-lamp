from wtforms import Form, TextAreaField, validators


# Post Form Class
class PostForm(Form):
    post = TextAreaField('Post', [validators.required(), validators.Length(min=4, max=180, message='Post must be between 4 and 180 characters')])