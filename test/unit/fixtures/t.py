import pytest
import re
from test.unit.strangler.helpers import strangler_log_file_delete


@pytest.fixture(autouse=True)
def t(request):
    """
    Yields a T fixture for every test function.
    For example
      def test_e61960(t):
          assert t.id == "e61960"
        ...
    """
    with T(request) as t:
        yield t


class T:

    def __init__(self, request):
        test_name = request.node.name  # eg  'test_e61960[3-4]' where [ starts parameters
        parts = re.split(r'_|\[', test_name)  # eg ['test', 'e61960', '3-4']
        assert len(parts[1]) == 6
        prefix = parts[1]
        self.id = prefix        # eg 'e61960'
        self.n = tally(prefix)  # eg 0

    def __enter__(self):
        strangler_log_file_delete()
        return self

    def __exit__(self, exc_type, _exc_value, _exc_traceback):
        pass


def tally(key):
    if key in _IDS:
        n = _IDS[key]
    else:
        n = _IDS[key] = 0
    _IDS[key] += 1
    return n + 1


_IDS = {}
