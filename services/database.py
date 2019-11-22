# encoding: utf8
import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id
# ================================================================================================
# Followers Table
# ================================================================================================


class Followers(db.Model):
    """Followers Table: 
    (A, B) -> User A follow user B 
    (A is the follower, B is the followed)"""
    __tablename__ = 'followers'
    followed_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed = relationship('User', foreign_keys='Followers.followed_id')

    follower_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), primary_key=True)
    follower = relationship('User', foreign_keys='Followers.follower_id')
