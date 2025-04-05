from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import SubmitField
from wtforms.validators import NumberRange
from wtforms.widgets.core import NumberInput


class UserForm(FlaskForm):

    min_message = IntegerField('min message', validators=[NumberRange(min=0)])
    min_rating = IntegerField('min rating', validators=[NumberRange(min=-10,max=10)])
    buy = IntegerField('min message', validators=[NumberRange(min=1)])
    submit = SubmitField('Change')
