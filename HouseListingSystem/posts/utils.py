from flask_mail import Message
from HouseListingSystem import mail


# send mail to notify owner that other user is interested in their house.
def send_mail(owner, interested_user, house):
    msg = Message('Interested in your house', sender='housesellingrenting@gmail.com', recipients=[owner.email])
    msg.body = f'''Hello {owner.name},

{interested_user.name} is interested in your {house.bhk} BHK {house.property_type} in {house.locality}, {house.city}.

{interested_user.name} would like to be contacted by you.
Contact Details:
Email : {interested_user.email}
Contact : {interested_user.contact} 

'''
    mail.send(msg)
