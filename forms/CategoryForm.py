from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms.validators import InputRequired, Length

class CategoryForm(FlaskForm):
    name = StringField('Category name', validators=[InputRequired(), Length(min=1, max=50)])