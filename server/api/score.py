from flask import request
from flask_restx import Namespace, Resource
from model import company_score
import json

ns = Namespace('company', description='Score operations')


class CompanyScoreApi(Resource):

    @ns.doc('Score a round in an XY Business Game')
    @ns.param(name="abc",
              description=("blah"))
    def get(self):
        data = list(request.args.keys())[0]
        kwargs = json.loads(data)
        return company_score(**kwargs)


def init_score_routes(api):
    api.add_namespace(ns, '/company')
    ns.add_resource(CompanyScoreApi, '/score/')
