from flask_wtf import FlaskForm
from wtforms import SubmitField


class ScoreForm(FlaskForm):

    def __init__(self, n, **kwargs):
        super().__init__(**kwargs)
        self.n = n

    submit = SubmitField('Score')
