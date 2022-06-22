import os
import secrets
from PIL import Image
from flask import render_template, redirect, flash, url_for, request, abort
from HouseListingSystem import app, db, bcrypt
from HouseListingSystem.models import User, House
from HouseListingSystem.forms import (RegisterForm, LoginForm,
                                      ResetPasswordRequestForm, ResetPasswordForm,
                                      UpdateAccountForm, PostHouseForm)
from flask_login import login_user, current_user, logout_user, login_required
from HouseListingSystem.email import send_mail


@app.route('/')
@app.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    page = request.args.get('page', 1, type=int)
    results = House.query.order_by(House.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', title='Home Page', results=results)


@app.route('/Register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, contact=form.contact.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Registered successful ! Now you can login", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/LogIn', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Log In successful for {user.name} !", 'success')
            return redirect(url_for('home'))
        else:
            flash(f"Log In unsuccessful. Please check username and password", 'danger')

    return render_template('login.html', title="LogIn", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Log Out Successfully', 'success')
    return redirect(url_for('login'))


@app.route('/ResetPasswordRequest', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_password_token()
            send_mail(token=token, user=user)
        flash('Password reset link has been sent to your email.', 'info')
    return render_template('reset_password_request.html', title='Request Password Reset', form=form)


@app.route('/ResetPassword/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if user is None:
        flash('That is invalid or expired token.', 'warning')
        return redirect(url_for('reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been reset! Now you can login", 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@login_required
@app.route('/ViewAccount')
def view_account():
    return render_template('view_account.html')


@app.route('/UpdateAccount', methods=['POST', 'GET'])
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.contact = form.contact.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('view_account'))
    else:
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.contact.data = current_user.contact
    return render_template('update_account.html', form=form)


@app.route('/DeleteAccount')
def delete_account():
    user = current_user
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Account deleted successfully!', 'success')
        return redirect(url_for('register'))
    except:
        flash('please delete all house posts first')
        return redirect(url_for('home'))


@app.route('/SellHouse', methods=['GET', 'POST'])
@login_required
def sell_house():
    form = PostHouseForm()
    if form.validate_on_submit():
        if form.house_image.data:
            img_file = save_picture(form.house_image.data)
            image_file = img_file
        else:
            image_file = 'house_default.jpg'
        post_type = 'Sell'
        price = form.price.data
        house = House(post_type=post_type, user=current_user, city=form.city.data, locality=form.locality.data,
                      address=form.address.data, image_file=image_file, bhk=form.bhk.data,
                      property_type=form.property_type.data, price=price, area=form.area.data)
        db.session.add(house)
        db.session.commit()
        flash('House posted successfully', 'success')
    return render_template('sell_house.html', title='Sell House', form=form)


@app.route('/RentHouse', methods=['GET', 'POST'])
@login_required
def rent_house():
    form = PostHouseForm()
    if form.validate_on_submit():
        if form.house_image.data:
            img_file = save_picture(form.house_image.data)
            image_file = img_file
        else:
            image_file = 'default.jpg'
        post_type = 'Rent'
        rent_per_month = form.rent_per_month.data
        house = House(post_type=post_type, user=current_user, city=form.city.data, locality=form.locality.data,
                      address=form.address.data, image_file=image_file, bhk=form.bhk.data,
                      property_type=form.property_type.data, rent_per_month=rent_per_month,
                      area=form.area.data)
        db.session.add(house)
        db.session.commit()
        flash('House posted successfully', 'success')
    return render_template('rent_house.html', title='Rent House', form=form)


@app.route('/MyPosts')
@login_required
def my_posts():
    page = request.args.get('page', 1, type=int)
    results = House.query.filter_by(user_id=current_user.user_id).order_by(House.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('my_posts.html', title='My Posts', results=results)


@app.route('/HousePost/<int:house_id>')
@login_required
def house_post(house_id):
    house = House.query.get_or_404(house_id)
    image_file = url_for('static', filename='images/' + house.image_file)
    return render_template('house_post.html', house=house, image_file=image_file)


@app.route('/HousePost/<int:house_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(house_id):
    house = House.query.get_or_404(house_id)
    if house.user != current_user:
        abort(403)
    form = PostHouseForm()
    if form.validate_on_submit():
        if form.house_image.data:
            img_file = save_picture(form.house_image.data)
            house.image_file = img_file
        house.bhk = form.bhk.data
        house.city = form.city.data
        house.locality = form.locality.data
        house.address = form.address.data
        house.area = form.area.data
        if house.post_type == 'Rent':
            house.rent_per_month = form.rent_per_month.data
        else:
            house.price = form.price.data
        db.session.commit()
        flash('Your house post has been updated!', 'success')
        return redirect(url_for('house_post', house_id=house.house_id))
    elif request.method == 'GET':
        form.bhk.data = house.bhk
        form.city.data = house.city
        form.locality.data = house.locality
        form.address.data = house.address
        form.area.data = house.area
        if house.post_type == 'Rent':
            form.rent_per_month.data = house.rent_per_month
        else:
            form.price.data = house.price
    image_file = url_for('static', filename='images/' + house.image_file)
    if house.post_type == 'Rent':
        return render_template('rent_house.html', title='Update House',
                               form=form, legend='Update House', image_file=image_file)
    else:
        return render_template('sell_house.html', title='Update House',
                               form=form, legend='Update House', image_file=image_file)


@app.route('/HousePost/<int:house_id>/delete')
@login_required
def delete_post(house_id):
    house = House.query.get_or_404(house_id)
    db.session.delete(house)
    db.session.commit()
    flash('House deleted successfully', 'success')
    return redirect(url_for('my_posts'))


def save_picture(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', image_fn)

    output_size = (300, 300)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(picture_path)
    return image_fn
