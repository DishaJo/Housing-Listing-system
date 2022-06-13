from flask import render_template, redirect, flash, url_for
from HouseListingSystem import app, db, bcrypt
from HouseListingSystem.models import User
from HouseListingSystem.forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user


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
        user = User(name=form.name.data, contact=form.contact.data, email=form.email.data, password=hashed_password)
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
            login_user(user)
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


@app.route('/ResetPassword')
def reset_password():
    pass
    # return render_template('reset_password.html')

