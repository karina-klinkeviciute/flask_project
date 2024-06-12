import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(80), nullable=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    user_profile = db.relationship('UserProfile', back_populates='user', uselist=False)
    posts = db.relationship('Post', back_populates='author')

    def __repr__(self):
        return f'User {self.email}'


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    display_name = db.Column(db.String(80))
    bio = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='user_profile')


post_tag_association = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='posts')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    tags = db.relationship('Tag', secondary=post_tag_association, back_populates='posts')

    def __str__(self):
        return self.title

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary=post_tag_association, back_populates='tags')

    def __repr__(self):
        return f'Tag {self.name}'


