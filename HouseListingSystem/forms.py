from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from HouseListingSystem.models import User


# def validate_password(password):
#     symbol = ['@', '*', '#', '&', '!', '$']
#     password = password.strip()
#     if password.find(' ') != -1:
#         raise ValidationError('Password can not have white space.')
#     if len(password) < 8 or len(password) > 20:
#         raise ValidationError('Password must have minimum 8 & maximum 20 characters.')
#     if not any(char.isdigit() for char in password):
#         raise ValidationError('Password should have at least 1 digit')
#     if not any(char.islower() for char in password):
#         raise ValidationError('Password should have at least 1 lowercase letter')
#     if not any(char.isupper() for char in password):
#         raise ValidationError('Password should have at least 1 uppercase letter')
#     if not any(char in symbol for char in password):
#         raise ValidationError(f'Password should have at least on special character from this {symbol}')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter Username."), Length(min=5, max=20)])
    name = StringField('Name', validators=[DataRequired(message="Please enter name"), Length(min=2, max=25)])
    contact = StringField('Contact no', validators=[DataRequired(message="Please enter contact"), Length(max=10)])
    email = EmailField('EmailID', validators=[DataRequired(message="Please enter email"), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter password")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message="Please enter confirm password"),
                                                 EqualTo('password',
                                                         message="Confirm password does not match with password")])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken.')

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
    email = EmailField('Email', validators=[DataRequired(message="Please enter email"), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter password"), Length(max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email is not registered.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(message="Please enter password")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message="Please enter confirm password"),
                                                 EqualTo('password',
                                                         message="Confirm password does not match with password")])
    submit = SubmitField('Reset Password')
