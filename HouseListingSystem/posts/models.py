from HouseListingSystem import db
from datetime import datetime


class House(db.Model):
    house_id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.String(20), nullable=False)
    bhk = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    locality = db.Column(db.String(30), nullable=False)
    address = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(20), nullable=False)
    area = db.Column(db.String(20), nullable=False)  # area in SqFt
    value = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(20), nullable=False, default='Available')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    like = db.relationship('Like', backref='house', lazy=True, cascade="all, delete-orphan")
    favourite = db.relationship('Favourite', backref='house', lazy=True, cascade="all, delete-orphan")
    interest = db.relationship('Interest', backref='house', lazy=True, cascade="all, delete-orphan")
    image = db.relationship('Images', backref='house', lazy=True, cascade="all, delete-orphan")
    comment = db.relationship('Comment', backref='house', lazy=True, cascade="all, delete-orphan")


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


class City(db.Model):
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)


class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)
    locality = db.Column(db.String(100), nullable=False)


class Images(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'), nullable=False)
    image_file = db.Column(db.String(200), nullable=False)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    comment_content = db.Column(db.Text, nullable=False)
