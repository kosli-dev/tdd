from flask_restx import Namespace, Resource

ns = Namespace('health', description='Health operations')


class HealthReady(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self):
        return "OK", 200


def init_health_routes(api):
    api.add_namespace(ns, '/health')
    ns.add_resource(HealthReady, '/ready')
