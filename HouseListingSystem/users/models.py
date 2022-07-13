from HouseListingSystem import app, db, login_manager
from flask_login import UserMixin
from time import time
import jwt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile = db.Column(db.String(200), default='https://res.cloudinary.com/disha-joshi/image/upload/v1657174356/default_uvzbrk.jpg')
    verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    house_post = db.relationship('House', backref='user', lazy=True, cascade="all, delete-orphan")
    like = db.relationship('Like', backref='user', lazy=True, cascade="all, delete-orphan")
    favourite = db.relationship('Favourite', backref='user', lazy=True, cascade="all, delete-orphan")
    interest = db.relationship('Interest', backref='user', lazy=True, cascade="all, delete-orphan")
    comment = db.relationship('Comment', backref='user', lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"User('{self.username}','{self.name}','{self.email}','{self.contact}')"

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.user_id, 'exp': time() + expires_in},
                          app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except ValueError:
            return
        return User.query.get(user_id)


