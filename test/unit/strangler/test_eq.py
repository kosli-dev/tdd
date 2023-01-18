import pytest
from strangler.check import *
from strangler.decorators import *
from .helpers import *
from helpers.unit.lib.scoped_env_var import ScopedEnvVar


def test_18011110(t):
    """OVERWRITE_ONLY"""
    @contract_checked_method('__eq__', use=OVERWRITE_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Eq(lambda: True)
            self.append = None
    d = Diff()

    assert d == d
    assert no_cc_logging()


def test_18011111(t):
    """APPEND_TEST On Same"""
    @contract_checked_method('__eq__', use=APPEND_TEST, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Eq(lambda: True)
            self.append = Eq(lambda: True)
    s = Same()

    assert s == s
    assert no_cc_logging()


def test_18011112(t):
    """APPEND_TEST On Different"""
    @contract_checked_method('__eq__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Eq(lambda: True)
            self.append = Eq(lambda: False)
    d = Diff()

    with pytest.raises(ContractDifference) as exc:
        d == d
    check_exc_log(exc.value, "Diff", '__eq__', 'True', 'False')
    assert no_cc_logging()


def test_18011113(t):
    """APPEND_TEST Off Different"""
    @contract_checked_method('__eq__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Eq(lambda: True)
            self.append = Eq(lambda: False)
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert d == d
    assert no_cc_logging()


def test_18011114(t):
    """OVERWRITE_MAIN Same"""
    @contract_checked_method('__eq__', use=OVERWRITE_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Eq(lambda: True)
            self.append = Eq(lambda: True)
    s = Same()

    assert s == s
    assert no_cc_logging()


def test_18011115(t):
    """OVERWRITE_MAIN Different"""
    @contract_checked_method('__eq__', use=OVERWRITE_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Eq(lambda: True)
            self.append = Eq(lambda: False)
    d = Diff()

    assert d == d
    check_cm_log('True', 'False')


def test_18011116(t):
    """APPEND_MAIN Different"""
    @contract_checked_method('__eq__', use=APPEND_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Eq(lambda: True)
            self.append = Eq(lambda: False)
    d = Diff()

    assert d != d
    check_cm_log('True', 'False')


def test_18011117(t):
    """APPEND_MAIN Same"""
    @contract_checked_method('__eq__', use=APPEND_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Eq(lambda: False)
            self.append = Eq(lambda: False)
    d = Diff()

    assert d != d
    assert no_cc_logging()


def test_18011118(t):
    """APPEND_ONLY"""
    @contract_checked_method('__eq__', use=APPEND_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = None
            self.append = Eq(lambda: True)
    d = Diff()

    assert d == d
    assert no_cc_logging()

# - - - - - - - - - - - - - - - - - - - - - - -


def check_cm_log(c, m):
    check_cc_log('Diff', '__eq__', c, m)


class Eq:
    def __init__(self, v):
        self.v = v

    def __eq__(self, _other):
        return self.v()

