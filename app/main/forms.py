from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Required, Email

class UpdateProfile(FlaskForm):

    bio = TextAreaField("Tell us about yourself", validators=[Required()])
    submit = SubmitField("Submit")

class BlogPostsForm(FlaskForm):

    title=StringField("title", validators=[Required()])
    blog_post=TextAreaField("BlogPost", validators=[Required()])
    submit=SubmitField("post")

class CommentsForm(FlaskForm):

    comment=TextAreaField("Comment", validators=[Required()])
    submit=SubmitField("post comment")

class SubscriberForm(FlaskForm):

    subscriber_email = StringField("Email", validators=[Required(), Email()])
    submit = SubmitField("Subscribe")

class BlogUpdateForm(FlaskForm):
    blog_post = TextAreaField("Update Blog_Post")
    submit = SubmitField("Update BlogPost")