from flask import render_template, redirect, url_for, request, Blueprint
from HouseListingSystem import db
from flask_login import current_user
from HouseListingSystem.models import House, Like
from HouseListingSystem.posts.forms import SearchForm

main = Blueprint('main', __name__)


# passing search form to navbar in layout
@main.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)


@main.route('/')
@main.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    page = request.args.get('page', 1, type=int)
    results = (db.session.query(House).outerjoin(Like, House.house_id == Like.house_id)
               .group_by(House.house_id).filter(House.user_id != current_user.user_id)
               .order_by(db.func.count(Like.house_id).desc()).paginate(page=page, per_page=3))

    return render_template('home.html', title='Home Page', results=results)