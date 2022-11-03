from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, SubmitField, StringField, BooleanField
from wtforms import Form as NoCsrfForm
from wtforms.validators import DataRequired, Length


class Org:
    squads = None


class Squad:
    letters = None
    is_word = None


class SquadForm(NoCsrfForm):
    letters = StringField('', validators=[DataRequired(), Length(min=5, max=5)])
    is_word = BooleanField()


class ScoreForm(FlaskForm):

    squads = FieldList(FormField(SquadForm, default=lambda: Squad()))
    is_sentence = BooleanField()
    is_profound = BooleanField()
    submit = SubmitField('Score')


