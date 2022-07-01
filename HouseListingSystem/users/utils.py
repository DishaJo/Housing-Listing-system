from flask import url_for
from flask_mail import Message
from HouseListingSystem import mail


def send_mail(token, user):
    msg = Message('Password Reset Request', sender='housesellingrenting@gmail.com', recipients=[user.email])
    link = url_for('users.reset_password', token=token, _external=True)
    msg.body = f'''Hello {user.name},
Link to reset your password is given below : 
{link}

This link will expire in 10 minutes.

If you did not request password reset, ignore this message.'''
    mail.send(msg)