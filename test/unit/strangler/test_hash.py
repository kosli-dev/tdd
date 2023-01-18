import pytest
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_method
from .helpers import *
from helpers.unit.lib.scoped_env_var import ScopedEnvVar


def test_18011200(t):
    """OVERWRITE_ONLY"""
    @contract_checked_method('__hash__', use=OVERWRITE_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Hash(lambda: 8877)
            self.append = None
    d = Diff()

    assert hash(d) == 8877
    assert no_cc_logging()


def test_18011201(t):
    """APPEND_TEST On Same"""
    @contract_checked_method('__hash__', use=APPEND_TEST, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Hash(lambda: 5)
            self.append = Hash(lambda: 5)
    s = Same()

    assert hash(s) == 5
    assert no_cc_logging()


def test_18011202(t):
    """APPEND_TEST On Different"""
    @contract_checked_method('__hash__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Hash(lambda: 69)
            self.append = Hash(lambda: 56)
    d = Diff()

    with pytest.raises(ContractDifference) as exc:
        hash(d)
    check_exc_log(exc.value, 'Diff', '__hash__', '69', '56')
    assert no_cc_logging()


def test_18011203(t):
    """APPEND_TEST Off Different"""
    @contract_checked_method('__hash__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Hash(lambda: 23)
            self.append = Hash(lambda: raiser())
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert hash(d) == 23
    assert no_cc_logging()


def test_18011204(t):
    """OVERWRITE_MAIN Same"""
    @contract_checked_method('__hash__', use=OVERWRITE_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Hash(lambda: 42)
            self.append = Hash(lambda: 42)
    s = Same()

    assert hash(s) == 42
    assert no_cc_logging()


def test_18011205(t):
    """OVERWRITE_MAIN Different"""
    @contract_checked_method('__hash__', use=OVERWRITE_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Hash(lambda: 51)
            self.append = Hash(lambda: raiser())
    d = Diff()

    assert hash(d) == 51
    check_cm_log('51', 'not-set')


def test_18011206(t):
    """APPEND_MAIN Different"""
    @contract_checked_method('__hash__', use=APPEND_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Hash(lambda: raiser())
            self.append = Hash(lambda: 45)
    d = Diff()

    assert hash(d) == 45
    check_cm_log('not-set', '45')


def test_18011207(t):
    """APPEND_MAIN Same"""
    @contract_checked_method('__hash__', use=APPEND_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Hash(lambda: 7)
            self.append = Hash(lambda: 7)
    s = Same()

    assert hash(s) == 7
    assert no_cc_logging()


def test_18011208(t):
    """APPEND_ONLY"""
    @contract_checked_method('__hash__', use=APPEND_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = None
            self.append = Hash(lambda: 1122)
    d = Diff()

    assert hash(d) == 1122
    assert no_cc_logging()


# - - - - - - - - - - - - - - - - - - - - - - -


def check_cm_log(c, m):
    check_cc_log('Diff', '__hash__', c, m)


class Hash:
    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return self.v()
