from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class twitterName(FlaskForm):
    # Validators and such
    twitName = StringField('TwitterName',
                           validators=[DataRequired(), Length(min=1, max=25)])
    submit = SubmitField('Enter Twitter Username')
