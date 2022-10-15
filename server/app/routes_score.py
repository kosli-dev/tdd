import model


def register_score_routes(app_blueprint):

    @app_blueprint.route('/score')
    def score():
        return model.score(), 200
