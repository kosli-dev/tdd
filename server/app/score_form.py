from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ScoreForm(FlaskForm):

    def __init__(self, n, **kwargs):
        super().__init__(**kwargs)
        self.n = n

    squadA = StringField('Squad-A', validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Score')
