from flask import render_template


def register_score_routes(app_blueprint):

    @app_blueprint.route('/score')
    def score():
        return render_template('score.html')
