from flask_restx import Namespace, Resource
from model import company_score

ns = Namespace('company', description='Score operations')


class CompanyScoreApi(Resource):

    @ns.doc('Score an XY Game play')
    @ns.param(name="...",
              description=("..."))
    def get(self):
        decisions = [('XYZZY', False), ('hello', True)]
        kwargs = {'is_sentence': False, 'is_profound': False}
        return company_score(*decisions, **kwargs)


def init_score_routes(ns):
    ns.add_resource(CompanyScoreApi, '/score/')
