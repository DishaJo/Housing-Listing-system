from flask import render_template, redirect, flash, url_for, request, abort, Blueprint
from HouseListingSystem import db, messages
from HouseListingSystem.users.models import User, Notification
from HouseListingSystem.posts.models import House, Like, Interest, Images, City, Comment
from HouseListingSystem.posts.forms import (PostHouseForm, UpdateHouseStatusForm,
                                            SearchForm, FilterForm, CommentForm)
from flask_login import current_user, login_required
from HouseListingSystem.posts.utils import send_mail
import cloudinary.uploader
import cloudinary.api
posts = Blueprint('posts', __name__)

admin = User.query.filter_by(is_admin=True).first()


@posts.route('/rent-house/<string:post_type>', methods=['GET', 'POST'])
@login_required
def post_house(post_type):
    form = PostHouseForm()
    if form.validate_on_submit():
        house = House(post_type=post_type, user=current_user, city=form.city.data, locality=form.locality.data,
                      address=form.address.data, bhk=form.bhk.data,
                      property_type=form.property_type.data, value=form.value.data, area=form.area.data)
        db.session.add(house)
        db.session.flush()
        # create notification
        text = f"New house posted by user : {current_user.username}"
        notification = Notification(type='new user', text=text, user_id=admin.user_id)
        db.session.add(notification)
        house_id = house.house_id
        if form.house_image.data:
            images = request.files.getlist('house_image')
            for i in images:
                upload_result = cloudinary.uploader.upload(i)
                image_file = upload_result["secure_url"]
                img = Images(image_file=image_file, house_id=house_id)
                db.session.add(img)
        else:
            image_file = 'https://res.cloudinary.com/disha-joshi/image/upload/v1657129931/house_default_i4lpdi.jpg'
            img = Images(image_file=image_file, house_id=house_id)
            db.session.add(img)
        db.session.commit()
        flash(messages.post_added, 'success')
        return redirect(url_for('main.home'))
    return render_template('post_house.html', title=post_type + ' House', form=form, post_type=post_type)


@posts.route('/house-post/<int:house_id>', methods=['GET', 'POST'])
@login_required
def house_post(house_id):
    comment_form = CommentForm()
    house = House.query.get_or_404(house_id)
    images = Images.query.filter_by(house_id=house.house_id)
    similar_houses = House.query.filter(House.house_id != house.house_id, House.user != current_user, House.city == house.city, House.locality==house.locality,
                                        House.post_type==house.post_type, House.bhk==house.bhk).limit(2).all()
    images_all = Images.query.all()
    comments = Comment.query.filter_by(house_id=house.house_id).all()
    form = UpdateHouseStatusForm()
    if form.validate_on_submit():
        return redirect(url_for('posts.update_status', house_id=house.house_id, status=form.status.data, ))
    return render_template('house_post.html', house=house, images=images, form=form,
                           similar_houses=similar_houses, images_all=images_all, comment_form=comment_form, comments=comments)


@posts.route('/add-comment/<int:house_id>', methods=['GET', 'POST'])
@login_required
def add_comment(house_id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(house_id=house_id, user_id=current_user.user_id,
                          comment_content=comment_form.comment_content.data)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added')
    return redirect(url_for('posts.house_post', house_id=house_id))


@posts.route('/delete-comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    house_id = comment.house_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted')
    return redirect(url_for('posts.house_post', house_id=house_id))


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
    form = PostHouseForm(obj=house)
    images = Images.query.filter(Images.house_id == house.house_id,
                                 Images.image_file != 'https://res.cloudinary.com/disha-joshi/image/upload/v1657129931/house_default_i4lpdi.jpg').all()
    if form.validate_on_submit():
        form.populate_obj(house)
        if form.house_image.data:
            images = request.files.getlist('house_image')
            for i in images:
                upload_result = cloudinary.uploader.upload(i)
                image_file = upload_result["secure_url"]
                img = Images(image_file=image_file, house_id=house_id)
                db.session.add(img)
        db.session.add(house)
        db.session.commit()
        flash(messages.post_updated, 'success')
        return redirect(url_for('posts.house_post', house_id=house.house_id))
    return render_template('update_post.html', title='Update Post', form=form,images=images, legend='Update House')


# class Post(MethodView):
#     def _get_item(self, house_id):
#         return self.House.query.get_or_404(house_id)
#
#     def get(self, house_id):
#         user = self._get_item(house_id)
#         return jsonify(item.to_json())


@posts.route('/delete-image/<int:image_id>')
@login_required
def delete_image(image_id):
    image = Images.query.get_or_404(image_id)
    house_id = image.house_id
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted', 'warning')
    return redirect(url_for('posts.update_post', house_id=house_id))


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
    images = Images.query.filter_by(house_id=house.house_id)
    return render_template('post_detail.html', title='Post Detail', house=house, images=images)


@posts.route('/verify-post/<int:house_id>')
@login_required
def verify_post(house_id):
    if not current_user.is_admin:
        abort(403)
    house = House.query.get_or_404(house_id)
    house.verified = True
    db.session.commit()
    flash(messages.verified_post, 'success')
    return redirect(url_for('posts.post_detail', house_id=house.house_id))


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
    cities = City.query.all()
    return dict(form=form, cities=cities)


@posts.route('/searched-results', methods=['POST', 'GET'])
@login_required
def searched_results():
    form = SearchForm()
    filter_form = FilterForm()
    if form.validate_on_submit():
        searched_word = form.search.data
        results = House.query.filter(House.user != current_user, (House.city.ilike('%'+searched_word+'%')) |
                                     (House.locality.ilike('%'+searched_word+'%')) | (House.property_type.ilike('%'+searched_word+'%')))
        images = Images.query.all()

        return render_template('searched_results.html', form=form, filter_form=filter_form,
                               searched_word=searched_word, results=results, images=images)

    return render_template('searched_results.html', form=form, filter_form=filter_form)


@posts.route('/filtered-searched-results/<string:searched_word>', methods=['POST', 'GET'])
@login_required
def filtered_results(searched_word):
    filter_form = FilterForm()
    kwargs = {}
    results = House.query.filter_by(**kwargs).filter(House.user != current_user)
    if filter_form.validate_on_submit():
        if filter_form.post_type.data != '--':
            kwargs['post_type'] = filter_form.post_type.data
        if filter_form.bhk.data != '--':
            kwargs['bhk'] = filter_form.bhk.data
        if filter_form.property_type.data != '--':
            kwargs['property_type'] = filter_form.property_type.data
        if len(filter_form.min_value.data) != 0 and len(filter_form.max_value.data) != 0:
            results = House.query.filter_by(**kwargs).filter(House.user != current_user,
                                                             House.value >= filter_form.min_value.data,
                                                             House.value <= filter_form.max_value.data,
                                                             ).all()
        elif len(filter_form.max_value.data) != 0:
            results = House.query.filter_by(**kwargs).filter(House.user != current_user,
                                                             House.value <= filter_form.max_value.data).all()
        elif len(filter_form.min_value.data) != 0:
            results = House.query.filter_by(**kwargs).filter(House.user != current_user,
                                                             House.value >= filter_form.min_value.data).all()
        else:
            results = House.query.filter_by(**kwargs).filter(House.user != current_user)
    images = Images.query.all()
    return render_template('searched_results.html', filter_form=filter_form,
                           searched_word=searched_word, images=images,
                           results=results)


@posts.route('/interested-in-house/<int:house_id>')
@login_required
def interested_in_house(house_id):
    house = House.query.get_or_404(house_id)
    interest = Interest(house_id=house_id, user_id=current_user.user_id)
    db.session.add(interest)
    db.session.commit()
    # send mail to house owner
    owner = house.user
    send_mail(owner=owner, interested_user=current_user, house=house)
    flash(messages.mail_sent_to_owner, 'success')
    return redirect(url_for('posts.house_post', house_id=house.house_id))


@posts.route('/show-interested-users/<int:house_id>')
@login_required
def show_interested_users(house_id):
    house = House.query.get_or_404(house_id)
    if current_user != house.user:
        abort(403)
    results = Interest.query.filter_by(house_id=house.house_id).all()
    return render_template('interested_users.html', title='Interested users', results=results)


