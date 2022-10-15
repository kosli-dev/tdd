from flask_restx import Namespace, Resource
from model import score

ns = Namespace('score', description='Score operations')


class ScoreApi(Resource):

    @ns.doc('Score an XY Game play')
    @ns.param(name="...",
              description=("..."))
    def get(self):
        return score()


def init_score_routes(ns):
    ns.add_resource(ScoreApi, '/score/')
