from flask import Blueprint
from .init_routes import init_routes


def get_api_blueprint():
    # The dynamic blueprint creation pattern is used
    # to enable multiple instantiations of the application
    # in automated tests
    return Blueprint('api', __name__)