from flask_wtf import FlaskForm
from wtforms import (StringField, ValidationError,
                     SubmitField, SelectField)
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from HouseListingSystem.posts.models import City


class PostHouseForm(FlaskForm):
    property_type = SelectField('Property_type', choices=['Flat', 'Independent House'])
    city = SelectField('Select City', choices=[city.city_name for city in City.query.all()])
    locality = StringField('Locality', validators=[DataRequired(message='Please enter locality.'), Length(max=100)])
    address = StringField('Address', validators=[DataRequired(message='Please enter address.'), Length(max=500)])
    bhk = SelectField('BHK', choices=['1', '2', '3', '4', '5+'])
    value = StringField('Value', validators=[DataRequired(), Length(max=20)])
    house_image = FileField('Upload Images', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    area = StringField('Area in sq.ft', validators=[DataRequired(message='Please enter area'), Length(max=10)])
    submit = SubmitField('Submit')

    def validate_area(self, area):
        if not area.data.isnumeric():
            raise ValidationError('Only Numeric value is allowed.')

    def validate_value(self, value):
        if not value.data.isnumeric():
            raise ValidationError('Only Numeric value is allowed.')


class UpdateHouseStatusForm(FlaskForm):
    status = SelectField('Select Status', choices=['Available', 'Rented', 'Sold'])
    submit = SubmitField('Update Status')


class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired(message='Please enter city name')])
    submit = SubmitField("Search")


class FilterForm(FlaskForm):
    post_type = SelectField('For', choices=['--', 'sell', 'rent'])
    bhk = SelectField('BHK', choices=['--', '1', '2', '3', '4', '5+'])
    property_type = SelectField('Property Type', choices=['--', 'Flat', 'Independent House'])
    min_value = StringField('Min Price/Rent')
    max_value = StringField('Max Price/Rent')
    submit = SubmitField('Apply')


class CommentForm(FlaskForm):
    comment_content = StringField(validators=[DataRequired(message='Please enter content')])
    submit = SubmitField("Submit")
