import pytest
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_method
from .helpers import *
from helpers.unit.lib.scoped_env_var import ScopedEnvVar


def test_18011700(t):
    """OVERWRITE_ONLY"""
    @contract_checked_method('__repr__', use=OVERWRITE_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Repr(lambda: 123)
            self.append = None
    d = Diff()

    assert repr(d) == "123"
    assert no_cc_logging()


def test_18011701(t):
    """APPEND_TEST On Same"""
    @contract_checked_method('__repr__', use=APPEND_TEST, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Repr(lambda: 5)
            self.append = Repr(lambda: 5)
    s = Same()

    assert repr(s) == "5"
    assert no_cc_logging()


def test_18011703(t):
    """APPEND_TEST On Different"""
    @contract_checked_method('__repr__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Repr(lambda: 69)
            self.append = Repr(lambda: 56)
    d = Diff()

    with pytest.raises(ContractDifference) as exc:
        repr(d)
    check_exc_log(exc.value, 'Diff', '__repr__', '69', '56')
    assert no_cc_logging()


def test_18011704(t):
    """APPEND_TEST Off Different"""
    @contract_checked_method('__repr__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Repr(lambda: 23)
            self.append = Repr(lambda: raiser())
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert repr(d) == '23'
    assert no_cc_logging()


def test_18011705(t):
    """OVERWRITE_MAIN Same"""
    @contract_checked_method('__repr__', use=OVERWRITE_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Repr(lambda: 42)
            self.append = Repr(lambda: 42)
    s = Same()

    assert repr(s) == "42"
    assert no_cc_logging()


def test_18011706(t):
    """OVERWRITE_MAIN Different"""
    @contract_checked_method("__repr__", use=OVERWRITE_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Repr(lambda: "ccc")
            self.append = Repr(lambda: "mmm")
    d = Diff()

    assert repr(d) == "ccc"
    check_cm_log('ccc', 'mmm')


def test_18011707(t):
    """APPEND_MAIN Different"""
    @contract_checked_method('__repr__', use=APPEND_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Repr(lambda: raiser())
            self.append = Repr(lambda: 45)
    d = Diff()

    assert repr(d) == '45'
    check_cm_log('not-set', '45')


def test_18011708(t):
    """APPEND_MAIN Same"""
    @contract_checked_method('__repr__', use=APPEND_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Repr(lambda: 7)
            self.append = Repr(lambda: 7)
    s = Same()

    assert repr(s) == '7'
    assert no_cc_logging()


def test_18011709(t):
    """APPEND_ONLY"""
    @contract_checked_method('__repr__', use=APPEND_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = None
            self.append = Repr(lambda: 987)
    d = Diff()

    assert repr(d) == "987"
    assert no_cc_logging()

# - - - - - - - - - - - - - - - - - - - - - - -


def check_cm_log(c, m):
    check_cc_log("Diff", "__repr__", c, m)


class Repr:
    def __init__(self, v):
        self.v = v

    def __repr__(self):
        return f"{self.v()}"
