"""Application server"""

from flask import Flask
from flask_restx import Api as RestXApi


def app():
    xy = Flask(__name__)
    init_api_blueprint(xy)
    init_app_blueprint(xy)
    return xy


def init_api_blueprint(xy):
    from api import get_api_blueprint
    api_blueprint = get_api_blueprint()

    #if config.app_settings.SWAGGER_USE_HTTPS:
    #     @property
    #     def specs_url(self):
    #         return url_for(self.endpoint('specs'), _external=True, _scheme='https')
    #
    #     RestXApi.specs_url = specs_url

    api = RestXApi(
        app=api_blueprint,
        doc='/doc/',
        title='XY Business Game API',
        version='1.0',
        description="<br>".join([
            "Jerry Weinberg's XY Business Game.",
            "Partially described in his book, Experiential Learning: Volume 4. Sample Exercises",
            "Available on LeanPub: https://leanpub.com/experientiallearning4sampleexercises"
        ])
    )

    from api.score import ns as ns_score
    api.add_namespace(ns_score, '/company')

    from api.score import init_score_routes
    init_score_routes(ns_score)

    xy.register_blueprint(api_blueprint, url_prefix='/api')


def init_app_blueprint(xy):
    import app
    app_blueprint = app.get_app_blueprint()

    app.register_health_routes(app_blueprint)
    app.register_score_routes(app_blueprint)

    xy.register_blueprint(app_blueprint)
