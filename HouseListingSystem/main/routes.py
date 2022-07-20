from flask import render_template, redirect, url_for, request, Blueprint, flash
from HouseListingSystem import db
from flask_login import current_user
from HouseListingSystem.posts.models import House, Like, Images, City
from HouseListingSystem.posts.forms import SearchForm, FilterForm

main = Blueprint('main', __name__)


# passing search form to navbar in layout
@main.context_processor
def layout():
    form = SearchForm()
    cities = City.query.all()
    return dict(form=form, cities=cities)


@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    filter_form = FilterForm()
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    page = request.args.get('page', 1, type=int)
    results = (db.session.query(House).outerjoin(Like, House.house_id == Like.house_id).group_by(House.house_id).filter(House.user_id != current_user.user_id).order_by(db.func.count(Like.house_id).desc()))
    images = Images.query.all()
    if filter_form.validate_on_submit():

        if filter_form.validate_on_submit():
            if filter_form.post_type.data != '--':
                print(filter_form.post_type.data)
                results = results.filter(House.post_type == filter_form.post_type.data)
            if filter_form.bhk.data != '--':
                results = results.filter(House.bhk == filter_form.bhk.data)
            if filter_form.property_type.data != '--':
                results = results.filter(House.property_type == filter_form.property_type.data)

            if len(filter_form.max_value.data) != 0:
                results = results.filter(House.value <= filter_form.max_value.data)
            if len(filter_form.min_value.data) != 0:
                results = results.filter(House.value >= filter_form.min_value.data)
            # if filter_form.verified:
            #     results = results.filter(House.verified == True)
    results = results.paginate(page=page, per_page=3)
    return render_template('home.html', title='Home Page', images=images, results=results, filter_form=filter_form)
