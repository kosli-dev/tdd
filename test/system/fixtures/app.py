import pytest
from .lib import *


@pytest.fixture
def app():
    yield APP()


class APP:

    def home(self):
        return http_get('/')

    def get_company_score(self, *, n=3):
        return http_get(f"/score/{n}")

    def post_company_score(self, json):
        n = 2  # len(kwargs["squads"])
        return http_post_json(f"/score/{n}", json)
