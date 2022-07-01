from flask import render_template, redirect, flash, url_for, request, abort, Blueprint
from HouseListingSystem import db, messages
from HouseListingSystem.models import House, Like
from HouseListingSystem.posts.forms import PostHouseForm, UpdateHouseStatusForm, SearchForm
from flask_login import current_user, login_required
from HouseListingSystem.posts.utils import save_picture


posts = Blueprint('posts', __name__)


@posts.route('/sell-house', methods=['GET', 'POST'])
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
        flash(messages.post_added, 'success')
        return redirect(url_for('main.home'))
    return render_template('sell_house.html', title='Sell House', form=form)


@posts.route('/rent-house', methods=['GET', 'POST'])
@login_required
def rent_house():
    form = PostHouseForm()
    if form.validate_on_submit():
        if form.house_image.data:
            img_file = save_picture(form.house_image.data)
            image_file = img_file
        else:
            image_file = 'house_default.jpg'
        post_type = 'Rent'
        rent_per_month = form.rent_per_month.data
        house = House(post_type=post_type, user=current_user, city=form.city.data, locality=form.locality.data,
                      address=form.address.data, image_file=image_file, bhk=form.bhk.data,
                      property_type=form.property_type.data, rent_per_month=rent_per_month,
                      area=form.area.data)
        db.session.add(house)
        db.session.commit()
        flash(messages.post_added, 'success')
        return redirect(url_for('main.home'))
    return render_template('rent_house.html', title='Rent House', form=form)


@posts.route('/house-post/<int:house_id>', methods=['GET', 'POST'])
@login_required
def house_post(house_id):
    house = House.query.get_or_404(house_id)
    form = UpdateHouseStatusForm()
    if form.validate_on_submit():
        return redirect(url_for('posts.update_status', house_id=house.house_id, status=form.status.data))
    return render_template('house_post.html', house=house, form=form)


@posts.route('/update_status/<int:house_id>/<status>')
@login_required
def update_status(house_id, status):
    house = House.query.get_or_404(house_id)
    house.status = status
    db.session.commit()
    flash(messages.status_updated, 'success')
    return redirect(url_for('posts.house_post', house_id=house.house_id))


@posts.route('/house-post/<int:house_id>/update', methods=['GET', 'POST'])
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
        flash(messages.post_updated, 'success')
        return redirect(url_for('posts.house_post', house_id=house.house_id))
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


@posts.route('/house-post/<int:house_id>/delete')
@login_required
def delete_post(house_id):
    house = House.query.get_or_404(house_id)
    db.session.delete(house)
    db.session.commit()
    flash(messages.post_deleted, 'success')
    return redirect(url_for('users.my_posts'))


# admin functions

@posts.route('/verified-posts')
@login_required
def verified_posts():
    if not current_user.is_admin:
        abort(403)
    else:
        page = request.args.get('page', 1, type=int)
        results = House.query.filter_by(verified=True).paginate(page=page, per_page=3)
        return render_template('posts_list.html', title='Verified Posts', results=results,
                               function='posts.verified_posts')


@posts.route('/unverified-posts')
@login_required
def unverified_posts():
    if not current_user.is_admin:
        abort(403)
    else:
        page = request.args.get('page', 1, type=int)
        results = House.query.filter_by(verified=False).paginate(page=page, per_page=3)
        return render_template('posts_list.html', title='Unverified Posts', results=results,
                               function='posts.unverified_posts')


@posts.route('/post-detail/<int:house_id>')
@login_required
def post_detail(house_id):
    if not current_user.is_admin:
        abort(403)
    house = House.query.get_or_404(house_id)
    return render_template('post_detail.html', title='Post Detail', house=house)


@posts.route('/verify-post/<int:house_id>')
@login_required
def verify_post(house_id):
    if not current_user.is_admin:
        abort(403)
    house = House.query.get_or_404(house_id)
    house.verified = True
    db.session.commit()
    flash(messages.verified_post, 'success')
    return render_template('post_detail.html', title='Post Detail', house=house)


@posts.route('/like-post/<int:house_id>', methods=['GET'])
@login_required
def like_post(house_id):
    house = House.query.get_or_404(house_id)
    like = Like.query.filter_by(user_id=current_user.user_id, house_id=house.house_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.user_id, house_id=house.house_id)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('main.home'))


# passing search form to navbar in layout
@posts.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)


@posts.route('/searched-results', methods=['POST'])
@login_required
def searched_results():
    form = SearchForm()
    if form.validate_on_submit():
        searched_word = form.search.data.capitalize()
        page = request.args.get('page', 1, type=int)

        results = House.query.filter(House.city.like('%'+searched_word+'%'), House.user_id != current_user.user_id).paginate(page=page, per_page=3)

        return render_template('searched_results.html', form=form, searched_word=searched_word,results=results)
    return redirect(url_for('main.home'))


