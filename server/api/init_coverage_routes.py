from flask_restx import Namespace, Resource
from coverage import Coverage
import os

ns = Namespace('coverage', description='Coverage operations')


class CoverageReport(Resource):
    def post(self):
        self._report()

    def _report(self):  # pragma: no cover
        cov = Coverage.current()
        xy_dir = os.environ.get("XY_DIR")
        cov.stop()
        cov.save()
        cov.combine(data_paths=[xy_dir])
        cov.html_report(directory=xy_dir+"/test/system/coverage")


def init_coverage_routes(api):
    api.add_namespace(ns, '/coverage')
    ns.add_resource(CoverageReport, '/report')