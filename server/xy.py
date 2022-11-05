from flask import Flask, url_for
from flask_restx import Api as RestXApi
import os
from api import get_api_blueprint, init_routes
from config import Config


def app():
    xy = Flask(__name__)
    xy.config.from_object(Config)
    xy.config['RESTX_VALIDATE'] = True
    init_jinja_variables(xy)
    init_api_blueprint(xy)
    init_app_blueprint(xy)
    return xy


def init_api_blueprint(xy):
    api_blueprint = get_api_blueprint()
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
    init_routes(api)
    xy.register_blueprint(api_blueprint, url_prefix='/api')


def init_app_blueprint(xy):
    import app
    xy_blueprint = app.get_app_blueprint()
    app.register_routes(xy_blueprint)
    xy.register_blueprint(xy_blueprint)


def git_commit_sha():
    return os.environ.get("GIT_COMMIT_SHA")


def bundle_css():
    return url_for('static', filename=f"scss/bundle.{git_commit_sha()}.css")


def bundle_js():
    return url_for('static', filename=f"js/bundle.{git_commit_sha()}.js")


def init_jinja_variables(xy):

    @xy.context_processor
    def jinja_variables():
        return dict(bundle_css=bundle_css(),
                    bundle_js=bundle_js())
