from flask import redirect, render_template, url_for
from .score_form import ScoreForm, Org, Squad
from .results import write_result, read_result


def register_routes(app_blueprint):

    @app_blueprint.route('/')
    def home():
        return redirect(url_for('app.score', n=3))

    @app_blueprint.route('/score/<int:n>', methods=['GET', 'POST'])
    def score(n):
        org = Org(n)
        form = ScoreForm(obj=org)
        if form.validate_on_submit():
            form.populate_obj(org)
            squads = data_from(form)
            sid = write_result(squads)
            return redirect(url_for('app.scores', sid=sid))
        else:
            return render_template('score.html', form=form)

    @app_blueprint.route('/scores/<sid>', methods=['GET'])
    def scores(sid):
        return render_template('scores.html', result=read_result(sid))


def data_from(form):
    def squad(squad_index, squad):
        return {
            "char": "ABCDEF"[squad_index],
            "letters": squad.letters.data,
            "is_word": squad.is_word.data
        }
    return {
        "squads": [squad(*item) for item in enumerate(form.squads)],
        "is_sentence": form.is_sentence.data,
        "is_profound": form.is_profound.data
    }
