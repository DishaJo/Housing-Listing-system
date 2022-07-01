from HouseListingSystem import app, db, login_manager
from flask_login import UserMixin
from time import time
from datetime import datetime
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
    verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    house_post = db.relationship('House', backref='user', lazy=True, cascade="all, delete-orphan")
    like = db.relationship('Like', backref='user', lazy=True, cascade="all, delete-orphan")
    favourite = db.relationship('Favourite', backref='user', lazy=True, cascade="all, delete-orphan")
    interest = db.relationship('Interest', backref='user', lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"User('{self.username}','{self.name}','{self.email}','{self.contact}','{self.user_image}')"

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


class House(db.Model):
    house_id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.String(20), nullable=False)
    bhk = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    locality = db.Column(db.String(30), nullable=False)
    address = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(20), nullable=False)
    area = db.Column(db.String(20), nullable=False)  # area in SqFt
    price = db.Column(db.String(20))
    rent_per_month = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    image_file = db.Column(db.String(100), nullable=False, default='house_default.jpg')
    status = db.Column(db.String(20), nullable=False, default='Available')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    like = db.relationship('Like', backref='house', lazy=True, cascade="all, delete-orphan")
    favourite = db.relationship('Favourite', backref='house', lazy=True, cascade="all, delete-orphan")
    interest = db.relationship('Interest', backref='house', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"House('{self.house_id}','{self.post_type}','{self.property_type}','{self.user_id}','{self.city}')"


class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'), nullable=False)


class Favourite(db.Model):
    favourite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'), nullable=False)


class Interest(db.Model):
    interest_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'), nullable=False)

