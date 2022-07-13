from flask import render_template, redirect, flash, url_for, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from HouseListingSystem import db, bcrypt
from HouseListingSystem.users.models import User
from HouseListingSystem.posts.models import House, Favourite, Images, City
from HouseListingSystem.users.forms import (RegisterForm, LoginForm, ResetPasswordRequestForm,
                                            ResetPasswordForm, UpdateAccountForm)
from HouseListingSystem.posts.forms import SearchForm
from HouseListingSystem.users.utils import send_mail
from HouseListingSystem import messages
import cloudinary.uploader
import cloudinary.api

users = Blueprint('users', __name__)


@users.context_processor
def layout():
    # passing search form to navbar in layout
    form = SearchForm()
    cities = City.query.all()
    return dict(form=form, cities=cities)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, contact=form.contact.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(messages.register_successful, 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Registration', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(messages.login_successful, 'success')
            return redirect(url_for('main.home'))
        else:
            flash(messages.login_unsuccessful, 'danger')

    return render_template('login.html', title="LogIn", form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash(messages.logout, 'success')
    return redirect(url_for('users.login'))


@users.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_password_token()
            send_mail(token=token, user=user)
            form.email.data = ''
        flash(messages.email_sent, 'info')
    return render_template('reset_password_request.html', title='Request Password Reset', form=form)


@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_password_token(token)
    if user is None:
        flash(messages.expired_token, 'warning')
        return redirect(url_for('users.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(messages.password_reset, 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@users.route('/view-account')
@login_required
def view_account():
    return render_template('view_account.html')


@users.route('/update-account', methods=['POST', 'GET'])
@login_required
def update_account():
    form = UpdateAccountForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.add(current_user)
        db.session.commit()
        flash(messages.account_updated, 'success')
        return redirect(url_for('users.view_account'))
    return render_template('update_account.html', form=form)


@users.route('/delete-account')
@login_required
def delete_account():
    if current_user.is_admin:
        flash(messages.admin_delete_unsuccessful, 'info')
        return redirect(url_for('main.home'))
    user = current_user
    db.session.delete(user)
    db.session.commit()
    flash(messages.account_deleted, 'success')
    return redirect(url_for('users.register'))


@users.route('/my-posts')
@login_required
def my_posts():
    page = request.args.get('page', 1, type=int)
    results = (House.query.filter_by(user_id=current_user.user_id)
               .order_by(House.date_posted.desc()).paginate(page=page, per_page=3))
    images = Images.query.all()
    return render_template('my_posts.html', title='My Posts', results=results, images=images)


@users.route('/add-to-favourites/<int:house_id>')
@login_required
def add_to_favourites(house_id):
    house = House.query.get_or_404(house_id)
    favourite = Favourite.query.filter_by(user_id=current_user.user_id, house_id=house.house_id).first()
    if favourite:
        db.session.delete(favourite)
        db.session.commit()
        flash(messages.removed_favourite, 'success')
    else:
        favourite = Favourite(user_id=current_user.user_id, house_id=house.house_id)
        db.session.add(favourite)
        db.session.commit()
        flash(messages.added_favourite, 'success')
    return redirect(url_for('posts.house_post', house_id=house.house_id))


@users.route('/my-favourites')
@login_required
def my_favourites():
    page = request.args.get('page', 1, type=int)
    results = (db.session.query(House).outerjoin(Favourite, House.house_id == Favourite.house_id)
               .group_by(House.house_id).filter(Favourite.user_id == current_user.user_id)
               .paginate(page=page, per_page=3))
    images = Images.query.all()
    return render_template('my_favourites.html', title='My Favourites', results=results, images=images)


# admin functions
@users.route('/admin-panel')
@login_required
def admin_panel():
    if not current_user.is_admin:
        abort(403)
    else:
        return render_template('admin_panel.html', title='Admin Panel')


@users.route('/verified-users')
@login_required
def verified_users():
    if not current_user.is_admin:
        abort(403)
    else:
        page = request.args.get('page', 1, type=int)
        results = User.query.filter_by(is_admin=False, verified=True).paginate(page=page, per_page=3)
        return render_template('users_list.html', title='Verified Users', results=results,
                               function='users.verified_users')


@users.route('/unverified-users')
@login_required
def unverified_users():
    if not current_user.is_admin:
        abort(403)
    else:
        page = request.args.get('page', 1, type=int)
        results = User.query.filter_by(is_admin=False, verified=False).paginate(page=page, per_page=3)
        return render_template('users_list.html', title='Unverified Users', results=results,
                               function='users.unverified_users')


@users.route('/user-detail/<int:user_id>')
@login_required
def user_detail(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', title='User Detail', user=user)


@users.route('/verify-user/<int:user_id>')
@login_required
def verify_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    user.verified = True
    db.session.commit()
    flash(messages.verified_user, 'success')
    return render_template('user_detail.html', title='User Detail', user=user)



