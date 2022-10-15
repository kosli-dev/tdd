

def register_health_routes(app_blueprint):

    @app_blueprint.route('/ready')
    def ready():
        return "OK", 200
