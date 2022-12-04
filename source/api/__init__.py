from flask import Blueprint
from .init_score_routes import init_score_routes
from .init_health_routes import init_health_routes


def init_routes(api):
    init_score_routes(api)
    init_health_routes(api)


def get_api_blueprint():
    # The dynamic blueprint creation pattern is used
    # to enable multiple instantiations of the application
    # in automated tests
    return Blueprint('api', __name__)