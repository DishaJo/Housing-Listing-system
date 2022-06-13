from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired
from HouseListingSystem.models import User

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Please enter name"), Length(min=2, max=15)])
    contact = StringField('Contact no', validators=[DataRequired(message="Please enter contact"), Length(max=10)])
    email = EmailField('EmailID', validators=[DataRequired(message="Please enter email"), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter password")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message="Please enter confirm password"), EqualTo('password',
            message="Confirm password does not match with password")])
    submit = SubmitField('Submit')

    def validate_contact(self, contact):
        if not contact.data.isdigit():
            raise ValidationError('Invalid Contact no.')
        user = User.query.filter_by(contact=contact.data).first()
        if user:
            raise ValidationError('This contact no is already registered.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Log In')