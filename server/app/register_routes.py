from flask import redirect, render_template, url_for
from .score_form import ScoreForm


def register_routes(app_blueprint):

    @app_blueprint.route('/ready')
    def ready():
        return "OK", 200

    @app_blueprint.route('/score/<n>', methods=['POST', 'GET'])
    def score(n):
        form = ScoreForm(n)
        if form.validate_on_submit():
            # Score the input, save score in /tmp/file against generated sid
            return redirect(url_for('app.scores', sid='ed783w'))
        else:
            return render_template('score.html', form=form)

    @app_blueprint.route('/scores/<sid>', methods=['GET'])
    def scores(sid):
        return render_template('scores.html')
