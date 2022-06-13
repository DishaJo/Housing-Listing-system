from HouseListingSystem import app, db, login_manager
from flask_login import UserMixin
from time import time
import jwt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.contact}')"

    def get_reset_password_token(self, expires_in = 600):
        return jwt.encode({'reset_password': self.user_id, 'exp': time() + expires_in},
                          app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(user_id)