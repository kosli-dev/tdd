from flask import Blueprint

# The dynamic blueprint creation pattern is used
# to enable multiple instantiations of the application
# in automated tests
get_api_v1_blueprint = lambda: Blueprint('api_v1', __name__)