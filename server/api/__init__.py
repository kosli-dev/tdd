from flask import Blueprint


def get_api_blueprint():
    # The dynamic blueprint creation pattern is used
    # to enable multiple instantiations of the application
    # in automated tests
    return Blueprint('api', __name__)