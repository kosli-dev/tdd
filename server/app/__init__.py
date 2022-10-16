from flask import Blueprint

from .health import register_health_routes
from .score import register_score_routes


def get_app_blueprint():
    return Blueprint('app', __name__, template_folder='templates')
