from flask_restx import Namespace, Resource
from model import company_score
import json

ns = Namespace('company', description='Score operations')

DESCRIPTION = json.dumps({
    "is_sentence": False,
    "is_profound": False,
    "decisions": (("XYZZY", False), ("hello", True))
})


class CompanyScore(Resource):

    @ns.doc('Score a round in an XY Business Game')
    @ns.param(name="kwargs", _in="body", description=DESCRIPTION)
    def post(self):
        return company_score(**ns.payload)


def init_score_routes(api):
    api.add_namespace(ns, '/company')
    ns.add_resource(CompanyScore, '/score/')
