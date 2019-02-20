from srv import db
from flask_login import UserMixin
from srv import login
from flask import flash

class User(UserMixin, db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def set_password(self, password):
        #self.password_hash = generate_password_hash(password)
        self.password_hash = password

    def check_password(self, password):
        #return check_password_hash(self.password_hash, password)
        return self.password_hash == password;
    def __repr__(self):
        return '<User {}>'.format(self.username) 


@login.user_loader
def load_user(id):
    return User.query.get(int(id))