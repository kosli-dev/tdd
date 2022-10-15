from flask_restx import Namespace, Resource
from model import Scorer

ns = Namespace('scorer', description='Scoring operations')


class ScorerApi(Resource):

    @ns.doc('Score an XY Game play')
    @ns.param(name="...",
              description=("..."))
    def get(self):
        return Scorer().score()


def init_scorer_routes(ns):
    ns.add_resource(ScorerApi, '/score/')
