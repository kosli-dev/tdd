from flask import Flask
from flask_restx import Api as RestXApi
from flask_assets import Environment, Bundle
import os
from pathlib import Path
from api import get_api_blueprint
from api.score import init_score_routes


def app():
    xy = Flask(__name__)
    assets = Environment(xy)
    assets.cache = webasset_cache_dir()
    assets.url = xy.static_url_path
    init_css(xy, assets)
    init_js(xy, assets)
    init_api_blueprint(xy)
    init_app_blueprint(xy)
    return xy


def init_api_blueprint(xy):
    api_blueprint = get_api_blueprint()

    # if config.app_settings.SWAGGER_USE_HTTPS:
    #     @property
    #     def specs_url(self):
    #         return url_for(self.endpoint('specs'), _external=True, _scheme='https')
    #
    #     RestXApi.specs_url = specs_url

    api = RestXApi(
        app=api_blueprint,
        doc='/doc/',
        title='XY Business Game API',
        version='1.0',
        description="<br>".join([
            "Jerry Weinberg's XY Business Game.",
            "Partially described in his book, Experiential Learning: Volume 4. Sample Exercises",
            "Available on LeanPub: https://leanpub.com/experientiallearning4sampleexercises"
        ])
    )
    init_score_routes(api)
    xy.register_blueprint(api_blueprint, url_prefix='/api')


def init_app_blueprint(xy):
    import app
    app_blueprint = app.get_app_blueprint()
    app.register_health_routes(app_blueprint)
    app.register_score_routes(app_blueprint)
    xy.register_blueprint(app_blueprint)


def webasset_cache_dir():
    path = f"/tmp/webasset-cache-{os.getpid()}"
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    return path


def init_css(xy, assets):
    css_files = asset_file_paths(xy, "css")
    css = Bundle(*css_files, filters='cssmin', output='bundle.css')
    assets.register('css', css)


def init_js(xy, assets):
    js_files = asset_file_paths(xy, "js")
    js = Bundle(*js_files, filters='jsmin', output='bundle.js')
    assets.register('js', js)


def asset_file_paths(app, dir_name):
    static_path = Path(f'{app.root_path}/static/{dir_name}')
    return [f'{static_path}/{file.name}' for file in static_path.iterdir()]
