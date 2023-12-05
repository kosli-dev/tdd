import logging
from flask import Flask, url_for
from flask_restx import Api as RestXApi
from api import get_api_blueprint, init_routes
from config import Config


def app():
    xy = Flask(__name__)
    init_logging(xy)
    xy.config.from_object(Config)
    xy.config['RESTX_VALIDATE'] = True
    init_jinja_variables(xy)
    init_api_blueprint(xy)
    init_app_blueprint(xy)
    return xy


def init_logging(xy):
    # https://www.javacodemonk.com/configure-logging-in-gunicorn-based-application-in-docker-container-9989b7db
    # https://trstringer.com/logging-flask-gunicorn-the-manageable-way/
    gunicorn_logger = logging.getLogger('gunicorn.error')
    xy.logger.handlers = gunicorn_logger.handlers
    xy.logger.setLevel(gunicorn_logger.level)
    formatter = logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d] [%(process)d] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    for handler in xy.logger.handlers:
        handler.setFormatter(formatter)


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


def main_css():
    return url_for('static', filename=f"scss/main.css")


def main_js():
    return url_for('static', filename=f"js/main.js")


def init_jinja_variables(xy):

    @xy.context_processor
    def jinja_variables():
        return dict(main_css=main_css(),
                    main_js=main_js())
