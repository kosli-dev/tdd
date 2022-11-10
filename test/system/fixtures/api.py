import pytest
from .lib import *


@pytest.fixture
def api():
    yield API()


class API:

    def health_ready(self):
        return http_get('/api/health/ready')

    def company_score(self, **kwargs):
        return http_post_json("/api/company/score/", kwargs)
