from HouseListingSystem import app, db, login_manager
from flask_login import UserMixin
from time import time
from datetime import datetime
import jwt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SellHouse(db.Model, UserMixin):
    sell_house_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(25), nullable=False)
    locality = db.Column(db.String(30), nullable=False)
    address = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(20), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    ready_to_move = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    sell_house_post = db.relationship('SellHouse', backref='author', lazy=True)

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.name}','{self.email}','{self.contact}','{self.user_image}')"

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.user_id, 'exp': time() + expires_in},
                          app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(user_id)