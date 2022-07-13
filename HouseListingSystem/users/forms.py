from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, EmailField, ValidationError,
                     SubmitField, BooleanField)
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed
from HouseListingSystem.users.models import User
from flask_login import current_user
import HouseListingSystem.messages as m


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message=m.enter_username),
                                                   Length(min=6, max=20,
                                                          message=m.password_length)])
    name = StringField('Name', validators=[DataRequired(message=m.enter_name), Length(min=2, max=25)])
    contact = StringField('Contact no', validators=[DataRequired(message=m.enter_contact), Length(max=10),
                                                    Regexp('[6-9][0-9]{9}', message=m.invalid_contact)])
    email = EmailField('EmailID', validators=[DataRequired(message=m.enter_email), Length(max=120)])
    password = PasswordField('Password', validators={DataRequired(message=m.enter_password),
                                                     Regexp(
                                                         '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$',
                                                         message=m.password_validation)})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message=m.enter_confirm_password),
                                                 EqualTo('password',
                                                         message=m.invalid_confirm_password)])

    submit = SubmitField('Submit')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(m.username_taken)

    def validate_contact(self, contact):
        if not contact.data.isdigit():
            raise ValidationError(m.invalid_contact)
        user = User.query.filter_by(contact=contact.data).first()
        if user:
            raise ValidationError(m.contact_registered)

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(m.email_registered)


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(m.enter_email), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(message=m.enter_password)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(m.email_not_registered)


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators={DataRequired(message=m.enter_password),
                                                     Regexp(
                                                         '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$',
                                                         message=m.password_validation)})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message=m.enter_confirm_password),
                                                 EqualTo('password',
                                                         message=m.invalid_confirm_password)])
    submit = SubmitField('Reset Password')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    name = StringField('Name', validators=[DataRequired(m.enter_name), Length(min=2, max=25)])

    email = StringField('Email', validators=[DataRequired(message=m.enter_email)])
    contact = StringField('Contact no', validators=[DataRequired(message=m.enter_contact),
                                                    Length(max=10), Regexp('[6-9][0-9]{9}', message=m.invalid_contact)])
    profile = FileField('Update Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg'], message=m.file_allowed)])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(m.username_taken)

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(m.email_registered)

    def validate_contact(self, contact):
        if not contact.data.isdigit():
            raise ValidationError(m.invalid_contact)
        if contact.data != current_user.contact:
            user = User.query.filter_by(email=contact.data).first()
            if user:
                raise ValidationError(m.contact_registered)
