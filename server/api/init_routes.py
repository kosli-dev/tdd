from flask_restx import Namespace, Resource
from model import company_score
import json

ns = Namespace('company', description='Score operations')


class CompanyScoreApi(Resource):

    example = json.dumps({
        "is_sentence": False,
        "is_profound": False,
        "decisions": [["XYZZY", False], ["hello", True]]
    })
    @ns.doc('Score a round in an XY Business Game')
    @ns.param(name="kwargs", _in="body", description=example)
    def post(self):
        return company_score(**ns.payload)


class CoverageWriteData(Resource):
    def post(self):
        from coverage import Coverage
        cov = Coverage.current()
        cov.stop()
        cov.save()
        cov.combine(data_paths=[self.xy_dir()])
        cov.html_report(directory=self.xy_dir()+"/test/system/coverage")

    def xy_dir(self):
        import os
        return os.environ.get("XY_DIR")


def init_routes(api):
    api.add_namespace(ns, '/company')
    ns.add_resource(CompanyScoreApi, '/score/')
    ns.add_resource(CoverageWriteData, '/coverage_write_data')
