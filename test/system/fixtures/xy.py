import pytest


@pytest.fixture
def xy():
    yield XY()


class XY:
    pass
