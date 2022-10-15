import pytest
import re


@pytest.fixture
def t(request):
    yield T(request)


class T:

    def __init__(self, request):
        test_name = request.node.name  # eg  'test_ede61960[3-4]' where [ starts parameters
        parts = re.split(r'_|\[', test_name)  # eg ['test', 'ede61960', '3-4']
        assert len(parts[1]) == 8
        prefix = parts[1]
        self.id = prefix        # eg 'ede61960'
        self.n = tally(prefix)  # eg 0


def tally(key):
    if key in IDS:
        n = IDS[key]
    else:
        n = IDS[key] = 0
    IDS[key] += 1
    return n + 1


IDS = {}
