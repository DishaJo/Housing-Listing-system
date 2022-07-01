from flask_wtf import FlaskForm
from wtforms import (StringField, ValidationError,
                     SubmitField, SelectField)
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class PostHouseForm(FlaskForm):
    property_type = SelectField('Property_type', choices=['Flat', 'Independent House'])
    city = StringField('City', validators=[DataRequired(message='Please enter city'), Length(max=50)])
    locality = StringField('Locality', validators=[DataRequired(message='Please enter locality.'), Length(max=100)])
    address = StringField('Address', validators=[DataRequired(message='Please enter address.'), Length(max=500)])
    bhk = SelectField('BHK', choices=['1', '2', '3', '4', '5+'])
    price = StringField('Price', validators=[Length(max=20)])
    rent_per_month = StringField('Rent Per Month', validators=[Length(max=20)])
    house_image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    area = StringField('Area in sq.ft', validators=[DataRequired(message='Please enter area'), Length(max=10)])
    submit = SubmitField('Submit')

    def validate_area(self, area):
        if not area.data.isnumeric():
            raise ValidationError('Only Numeric value is allowed.')


class UpdateHouseStatusForm(FlaskForm):
    status = SelectField('Select Status', choices=['Available', 'Rented', 'Sold'])
    submit = SubmitField('Update Status')


class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired(message='Please enter city name')])
    submit = SubmitField("Search")