from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, EmailField, ValidationError,
                     SubmitField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Length, EqualTo
from HouseListingSystem.models import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter Username."), Length(min=5, max=20)])
    name = StringField('Name', validators=[DataRequired(message="Please enter name"), Length(min=2, max=25)])
    contact = StringField('Contact no', validators=[DataRequired(message="Please enter contact"),
                                                    Length(min=10, max=10, message='Contact should be of 10 digits')])
    email = EmailField('EmailID', validators=[DataRequired(message="Please enter email"), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter password"), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message="Please enter confirm password"),
                                                 EqualTo('password',
                                                         message="Confirm password does not match with password")])
    submit = SubmitField('Submit')

    # def validate_password(self, password):
    #     symbol = ['@', '*', '#', '&', '!', '$']
    #     password = password.data.strip()
    #     errors = ''
    #     if password.find(' ') != -1:
    #         errors += 'Password can not have white space.\n'
    #     # if len(password.data) < 6 or len(password.data) > 20:
    #     #     errors += 'Password must have minimum 6 & maximum 20 characters.\n'
    #     if not any(char.isdigit() for char in password.data):
    #         errors += 'Password should have at least 1 digit\n'
    #     if not any(char.islower() for char in password.data):
    #         errors += 'Password should have at least 1 lowercase letter\n'
    #     if not any(char.isupper() for char in password.data):
    #         errors += 'Password should have at least 1 uppercase letter\n'
    #     if not any(char in symbol for char in password.data):
    #         errors += f'Password should have at least on special character from this {symbol}\n'
    #     if errors != '':
    #         raise ValidationError(f'{errors}')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

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
    password = PasswordField('Password', validators=[DataRequired(message="Please enter password")])
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
    password = PasswordField('Password', validators=[DataRequired(message="Please enter password"), Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message="Please enter confirm password"),
                                                 EqualTo('password',
                                                         message="Confirm password does not match with password")])
    submit = SubmitField('Reset Password')

    # def validate_password(self, password):
    #     symbol = ['@', '*', '#', '&', '!', '$']
    #     password = password.data.strip()
    #     errors = ''
    #     if password.find(' ') != -1:
    #         errors += 'Password can not have white space.\n'
    #     # if len(password.data) < 6 or len(password.data) > 20:
    #     #     errors += 'Password must have minimum 6 & maximum 20 characters.\n'
    #     if not any(char.isdigit() for char in password.data):
    #         errors += 'Password should have at least 1 digit\n'
    #     if not any(char.islower() for char in password.data):
    #         errors += 'Password should have at least 1 lowercase letter\n'
    #     if not any(char.isupper() for char in password.data):
    #         errors += 'Password should have at least 1 uppercase letter\n'
    #     if not any(char in symbol for char in password.data):
    #         errors += f'Password should have at least on special character from this {symbol}\n'
    #     if errors != '':
    #         raise ValidationError(f'{errors}')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    name = StringField('Name', validators=[DataRequired(message="Please enter name"), Length(min=2, max=25)])

    email = StringField('Email', validators=[DataRequired()])
    contact = StringField('Contact no', validators=[DataRequired(message="Please enter contact"),
                                                    Length(min=10, max=10, message='Contact should be of 10 digits')])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    def validate_contact(self, contact):
        if not contact.data.isdigit():
            raise ValidationError('Invalid Contact no.')
        if contact.data != current_user.contact:
            user = User.query.filter_by(email=contact.data).first()
            if user:
                raise ValidationError('This contact no. is already registered.')


class PostSellHouseForm(FlaskForm):
    property_type = SelectField('Property_type', choices=['Flat', 'Independent House'])
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    locality = StringField('Locality', validators=[DataRequired(), Length(max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(max=500)])
    bhk = SelectField('BHK', choices=['1', '2', '3', '4', '5+'])
    price = StringField('Price', validators=[DataRequired(), Length(max=10)])
    extension = SelectField(choices=['Thousand', 'Lakh', 'Corer'])
    size = StringField('Size', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Submit')


