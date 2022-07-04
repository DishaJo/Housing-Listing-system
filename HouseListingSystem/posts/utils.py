import os
import secrets
from flask import current_app
from PIL import Image
from flask_mail import Message
from HouseListingSystem import mail


def save_picture(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', image_fn)

    output_size = (300, 300)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(picture_path)
    return image_fn


# send mail to notify owner that other user is interested in their house.
def send_mail(owner, interested_user, house):
    msg = Message('Interested in your house', sender='housesellingrenting@gmail.com', recipients=[owner.email])
    msg.body = f'''Hello {owner.name},

{ interested_user.name } is interested in your { house.bhk } BHK { house.property_type } in { house.locality }, { house.city }.

{ interested_user.name } would like to be contacted by you.
Contact Details:
Email : {interested_user.email}
Contact : {interested_user.contact} 

'''
    mail.send(msg)
