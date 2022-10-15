import pytest


@pytest.fixture
def xy():
    yield XY()


class XY:
    def score(self):
        # TODO: call score through API
        return {"A": 23, "B": 1245, "C": 78}
