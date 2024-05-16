from flask_wtf import FlaskForm

from models import Category
from wtforms import StringField, FloatField, SelectField, validators
from wtforms.validators import InputRequired, Length

class ExpenseForm(FlaskForm):
    name = StringField('Expense name', validators=[InputRequired(), Length(min=1, max=50)])
    value = FloatField('Price', validators=[InputRequired(), validators.NumberRange(min=0.01)])
    category = SelectField('Category', coerce=int)

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]


