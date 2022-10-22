from flask import Blueprint
from .init_score_routes import init_score_routes
from .init_coverage_routes import init_coverage_routes


def get_api_blueprint():
    # The dynamic blueprint creation pattern is used
    # to enable multiple instantiations of the application
    # in automated tests
    return Blueprint('api', __name__)