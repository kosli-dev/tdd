import pytest
from .lib import *


@pytest.fixture
def app():
    yield APP()


class APP:

    def company_score(self, **kwargs):
        return http_get("/score/4", **kwargs)
