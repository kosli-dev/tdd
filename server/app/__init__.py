from flask import Blueprint

from .register_routes import register_routes


def get_app_blueprint():
    return Blueprint('app', __name__, template_folder='templates')
