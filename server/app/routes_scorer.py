from model import Scorer


def register_scorer_routes(app_blueprint):

    @app_blueprint.route('/scorer')
    def score():
        points = Scorer().score()
        return points, 200
