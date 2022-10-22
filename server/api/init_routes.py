from flask_restx import Namespace, Resource
from model import company_score
from coverage import Coverage
import json
import os

ns = Namespace('company', description='Score operations')

DESCRIPTION = json.dumps({
    "is_sentence": False,
    "is_profound": False,
    "decisions": [["XYZZY", False], ["hello", True]]
})


class CompanyScoreApi(Resource):

    @ns.doc('Score a round in an XY Business Game')
    @ns.param(name="kwargs", _in="body", description=DESCRIPTION)
    def post(self):
        return company_score(**ns.payload)


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


def init_routes(api):
    api.add_namespace(ns, '/company')
    ns.add_resource(CompanyScoreApi, '/score/')
    ns.add_resource(CoverageReport, '/coverage_report')
