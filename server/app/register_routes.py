from flask import render_template


def register_routes(app_blueprint):

    @app_blueprint.route('/ready')
    def ready():
        return "OK", 200

    @app_blueprint.route('/xy')
    def xy():
        return render_template('xy.html')

    @app_blueprint.route('/scores')
    def scores():
        return render_template('scores.html')
