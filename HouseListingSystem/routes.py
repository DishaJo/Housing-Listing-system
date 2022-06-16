from flask import render_template, redirect, flash, url_for
from HouseListingSystem import app, db, bcrypt
from HouseListingSystem.models import User
from HouseListingSystem.forms import RegisterForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user
from HouseListingSystem.email import send_mail


@app.route('/')
@app.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/Register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        check = User.query.filter_by(email=form.email.data).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, contact=form.contact.data, email=form.email.data, password=hashed_password)
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


@app.route('/PostProperty')
def post_property():
    return "PostProperty"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# def send_password_reset_email(user):
#     pass


@app.route('/ResetPasswordRequest', methods=['GET','POST'])
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
