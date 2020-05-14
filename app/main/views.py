from flask import render_template, redirect, request, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from . import forms
from ..models import User, BlogPosts, Comments, Subscriber
from .forms import UpdateProfile, BlogPostsForm, CommentsForm, SubscriberForm, BlogUpdateForm
from .. import db
from ..requests import get_quotes
from ..email import Message, mail_message
from .. import email

# @main.route("/movie/review/new/<int:id>", methods = ["GET", "POST"])
# @login_required
# def new_review(id):

@main.route("/", methods=["GET", "POST"])
def index():
    blog_posts=BlogPosts.get_all_blogposts()
    title="Blogs Mania"
    quotes=get_quotes()
    print(quotes)

    subscribe_form = SubscriberForm()
    if subscribe_form.validate_on_submit():
        subscriber = Subscriber(email=subscribe_form.subscriber_email.data)

        db.session.add(subscriber)
        db.session.commit()

        # flash("Thankyou for subscribing to our news letter")

        return redirect(url_for("main.index"))

    return render_template("index.html", blog_posts=blog_posts, title=title, quotes=quotes, subscribe_form=subscribe_form)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    id=current_user.id
    user_blog_posts = BlogPosts.get_user_blogposts(id)
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)
    
    return render_template("profile/profile.html", user = user, user_blog_posts=user_blog_posts)

@main.route("/user/<uname>/update", methods = ["GET", "POST"])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname = user.username))
    
    return render_template('profile/update_profile.html', form = form)

@main.route("/blogpost", methods=["GET", "POST"])
@login_required
def new_blogpost():
    blogposts_form=BlogPostsForm()
    subscribers = Subscriber.get_all_subscribers()
    if blogposts_form.is_submitted():
        title=blogposts_form.title.data
        blog_post=blogposts_form.blog_post.data
        users_id=current_user.id

        blog_posts=BlogPosts(title=title, blog_post=blog_post, users_id=users_id)

        db.session.add(blog_posts)
        db.session.commit()
        # import pdb; pdb.set_trace()
        recipients=[]
        for obj in subscribers:
            recipients.append(obj.email)

        email.mail_message(to=[obj.email for obj in subscribers],subject=title,body=render_template('email/new_post.txt'),html=render_template('email/new_post.html'))
        # (to=[obj.em,templateail for obj in subscribers])

        for subscribe in subscribers:
            mail_message = ("A New Post has been posted", "email/new_post", subscribe.email)
            print(mail_message)

        return redirect(url_for('main.new_blogpost'))

    title='new blogpost'
    return render_template('blogposts/new_blogpost.html', blogposts_form=blogposts_form, title=title)

@main.route("/blogpost/<int:blog_id>", methods=["GET", "POST"])
def single_blog_post(blog_id):
    blog_post = BlogPosts.get_single_blogpost(blog_id)
    # import pdb; pdb.set_trace()
    comments = Comments.get_comments(blog_id)
    comments_form=CommentsForm()
    if comments_form.is_submitted():
        comment=comments_form.comment.data
        user_id=current_user.id
        blogs_id=blog_id

        save_comments=Comments(comment=comment, user_id=user_id, blogs_id=blogs_id)

        db.session.add(save_comments)
        db.session.commit()

    return render_template("blogposts/single_blogpost.html", blog_post=blog_post, comments_form=comments_form, comments=comments)

@main.route('/blogpost/<int:blog_id>/delete')
def delete(blog_id):
    # Comments.query.filter_by(id=blog_id).delete()
    post = BlogPosts.query.filter_by(id=blog_id).delete()
    # import pdb; pdb.set_trace()
    # db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))

# @main.route('/subscribe')
# def subscribe():
    
    
#     return render_template("")

@main.route("/blogpost/<int:blog_id>/update", methods=["GET", "POST"])
def update(blog_id):

    blog_update = BlogUpdateForm()
    # blogpost = BlogPosts.query.filter_by(blog_id).first()
    blogpost = BlogPosts.update_blogpost(blog_id)

    if blog_update.is_submitted():
        blogpost.blog_post = blog_update.blog_post.data
        db.session.commit()

        return redirect(url_for("main.single_blog_post", blog_id=blog_id))
    
    return render_template("/blogposts/update_blogpost.html", blog_update=blog_update)