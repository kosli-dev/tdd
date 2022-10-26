from flask import redirect, render_template, url_for
from .score_form import ScoreForm
from .results import write_result, read_result


def register_routes(app_blueprint):

    @app_blueprint.route('/ready')
    def ready():
        return "OK", 200

    @app_blueprint.route('/score/<n>', methods=['POST', 'GET'])
    def score(n):
        form = ScoreForm(n)
        if form.validate_on_submit():
            # TODO: Score the input, generate a sid
            sid = 'ed783w'
            write_result(sid, FAKE_RESULT)
            return redirect(url_for('app.scores', sid=sid))
        else:
            return render_template('score.html', form=form)

    @app_blueprint.route('/scores/<sid>', methods=['GET'])
    def scores(sid):
        return render_template('scores.html', result=read_result(sid))


FAKE_RESULT = {
    "squads": [
        {"char": "A", "letters": "xyzzy", "points": [4, 4, 15, 5, 6], "total": 34},
        {"char": "B", "letters": "hello", "points": [25, 25, 2, 2, 0], "total": 54},
        {"char": "C", "letters": "world", "points": [11, 11, 11, 11, 11], "total": 55},
    ],
    "total_score": 143
}
