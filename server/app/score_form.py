from flask_wtf import FlaskForm
from wtforms import SubmitField


class ScoreForm(FlaskForm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    submit = SubmitField('Score')
