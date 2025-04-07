from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import SubmitField
from wtforms.validators import NumberRange
from wtforms.widgets.core import NumberInput


class UserForm(FlaskForm):

    #names of the variables must be same as names of keys in USERDATAMANAGER
    min_news = IntegerField('min news', validators=[NumberRange(min=0)])
    min_score = IntegerField('min rating', validators=[NumberRange(min=-10,max=10)])
    buy = IntegerField('buy stock', validators=[NumberRange(min=1)])
    days_back = IntegerField('days back', validators=[NumberRange(min=1,max=364)],description="test")
    submit = SubmitField('Change')
