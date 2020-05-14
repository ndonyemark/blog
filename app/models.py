from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .import login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    blog_posts=db.relationship("BlogPosts", backref='users', lazy="dynamic")
    comments=db.relationship("Comments", backref='users', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref = 'role', lazy = "dynamic")

    def __repr__(self):
        return f'User {self.name}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class BlogPosts(db.Model):
    __tablename__ = "blogposts"
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(255))
    blog_post=db.Column(db.Text)
    date_posted=db.Column(db.DateTime, default=datetime.utcnow)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments=db.relationship("Comments", backref='blogposts' , lazy="dynamic")

    @classmethod
    def get_single_blogpost(cls,blog_id):
        blog = BlogPosts.query.filter_by(id=blog_id).first()
        return blog
    
    @classmethod
    def get_all_blogposts(cls):
        blog=BlogPosts.query.all()
        return blog
    
    @classmethod
    def get_user_blogposts(cls,user_id):
        blog=BlogPosts.query.filter_by(users_id=user_id).all()
        return blog
    
    @classmethod
    def update_blogpost(cls, blog_id):
        blog = BlogPosts.query.filter_by(id=blog_id).first()
        return blog

    def __repr__(self):
        return self

class Comments(db.Model):
    __tablename__="comments"
    id=db.Column(db.Integer, primary_key=True)
    comment=db.Column(db.Text)
    date_posted=db.Column(db.DateTime, default=datetime.utcnow)
    user_id=db.Column(db.Integer,  db.ForeignKey('users.id'))
    blogs_id=db.Column(db.Integer, db.ForeignKey('blogposts.id', ondelete='CASCADE'))

    @classmethod
    def get_comments(cls,blog_id):
        comments=Comments.query.filter_by(blogs_id=blog_id).all()
        return comments

class Quotes:

    def __init__(self, author, quote, permalink):
        self.author = author
        self.quote = quote
        self.permalink = permalink

class Subscriber(db.Model):

    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))

    @classmethod
    def get_all_subscribers(cls):
        subscribers = Subscriber.query.all()
        return subscribers