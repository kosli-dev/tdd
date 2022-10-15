from flask import Blueprint

from .routes_health import register_health_routes
from .routes_score import register_score_routes


def get_app_blueprint():
    return Blueprint('app', __name__, template_folder='templates')
