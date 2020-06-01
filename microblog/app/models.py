from app import login
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)



    @staticmethod
    def make_unique_username(username):
        if User.query.filter_by(username=username).first() == None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.query.filter_by(username=new_username).first() == None:
                break
            version += 1
        return new_username




    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))





from datetime import datetime
from flask_login import UserMixin
from sweater import db, manager


class Tickets(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    from_city = db.Column(db.String(300), nullable=False)
    to_city = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.Date)
class hisoriTickets(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    login_id = db.Column(db.Integer())
    from_city = db.Column(db.String(300), nullable=False)
    to_city = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.Date)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(200),nullable=False)



@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
