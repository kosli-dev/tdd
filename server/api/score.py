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


def init_score_routes(api):
    api.add_namespace(ns, '/company')
    ns.add_resource(CompanyScoreApi, '/score/')
