

def register_score_routes(app_blueprint):

    @app_blueprint.route('/score')
    def score():
        html = "".join([
            "<html>",
            "<head></head>",
            "<body>",
            "Jerry Weinberg's XY Business Game",
            "</body>",
            "</html>"
        ])
        return html, 200
