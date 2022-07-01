import os
import secrets
from flask import current_app
from PIL import Image


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