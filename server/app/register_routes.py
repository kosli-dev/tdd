from flask import redirect, render_template, url_for
from .score_form import ScoreForm


def register_routes(app_blueprint):

    @app_blueprint.route('/ready')
    def ready():
        return "OK", 200

    @app_blueprint.route('/score', methods=['POST', 'GET'])
    def score():
        form = ScoreForm()
        if form.validate_on_submit():
            return redirect(url_for('app.scores'))
        else:
            return render_template('score.html', form=form)

    @app_blueprint.route('/scores', methods=['GET'])
    def scores():
        return render_template('scores.html')
