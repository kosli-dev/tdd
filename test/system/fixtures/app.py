import pytest
from .lib import *


@pytest.fixture
def app():
    yield APP()


class APP:

    def home(self):
        return http_get('/')

    def company_score(self, *, n):
        return http_get(f"/score/{n}")
