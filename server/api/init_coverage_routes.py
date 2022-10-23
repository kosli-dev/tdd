from flask_restx import Namespace, Resource
from coverage import Coverage

ns = Namespace('coverage', description='Coverage operations')


class CoverageSave(Resource):  # pragma: no cover
    # noinspection PyMethodMayBeStatic
    def post(self):
        cov = Coverage.current()
        if cov:
            cov.stop()
            cov.save()


def init_coverage_routes(api):
    api.add_namespace(ns, '/coverage')
    ns.add_resource(CoverageSave, '/save')
