"""Application server"""

from flask import Flask, url_for
from flask_restx import Api as RestXApi


def create_app():
    app = Flask(__name__)
    init_api_v1_blueprint(app)
    init_app_blueprint(app)
    return app


def init_api_v1_blueprint(app):
    from apis.v1 import get_api_v1_blueprint
    api_blueprint = get_api_v1_blueprint()

    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

    RestXApi.specs_url = specs_url

    api = RestXApi(
        app=api_blueprint,
        doc='/doc/',
        title='XY Business Game API',
        version='1.0',
        description="Jerry Weinberg's XY Business Game",
    )

    from apis.v1.scorer import ns as ns_scorer
    api.add_namespace(ns_scorer, '/score')

    from apis.v1.scorer import init_scorer_routes
    init_scorer_routes(ns_scorer)

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')


def init_app_blueprint(server):
    import app
    app_blueprint = app.get_app_blueprint()

    app.register_health_routes(app_blueprint)
    app.register_scorer_routes(app_blueprint)

    server.register_blueprint(app_blueprint)
