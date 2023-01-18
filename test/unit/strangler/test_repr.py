import pytest
from strangler import *
from .helpers import *


def test_18011700(t):
    """OLD_ONLY"""
    @strangled_method('__repr__', use=OLD_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.old = Repr(lambda: 123)
            self.new = None
    d = Diff()

    assert repr(d) == "123"
    assert no_cc_logging()


def test_18011701(t):
    """NEW_TEST On Same"""
    @strangled_method('__repr__', use=NEW_TEST, kind="query")
    class Same:
        def __init__(self):
            self.old = Repr(lambda: 5)
            self.new = Repr(lambda: 5)
    s = Same()

    assert repr(s) == "5"
    assert no_cc_logging()


def test_18011703(t):
    """NEW_TEST On Different"""
    @strangled_method('__repr__', use=NEW_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.old = Repr(lambda: 69)
            self.new = Repr(lambda: 56)
    d = Diff()

    with pytest.raises(StrangledDifference) as exc:
        repr(d)
    check_exc_log(exc.value, 'Diff', '__repr__', '69', '56')
    assert no_cc_logging()


def test_18011704(t):
    """NEW_TEST Off Different"""
    @strangled_method('__repr__', use=NEW_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.old = Repr(lambda: 23)
            self.new = Repr(lambda: raiser())
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert repr(d) == '23'
    assert no_cc_logging()


def test_18011705(t):
    """OLD_MAIN Same"""
    @strangled_method('__repr__', use=OLD_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.old = Repr(lambda: 42)
            self.new = Repr(lambda: 42)
    s = Same()

    assert repr(s) == "42"
    assert no_cc_logging()


def test_18011706(t):
    """OLD_MAIN Different"""
    @strangled_method("__repr__", use=OLD_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.old = Repr(lambda: "ccc")
            self.new = Repr(lambda: "mmm")
    d = Diff()

    assert repr(d) == "ccc"
    check_cm_log('ccc', 'mmm')


def test_18011707(t):
    """NEW_MAIN Different"""
    @strangled_method('__repr__', use=NEW_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.old = Repr(lambda: raiser())
            self.new = Repr(lambda: 45)
    d = Diff()

    assert repr(d) == '45'
    check_cm_log('not-set', '45')


def test_18011708(t):
    """NEW_MAIN Same"""
    @strangled_method('__repr__', use=NEW_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.old = Repr(lambda: 7)
            self.new = Repr(lambda: 7)
    s = Same()

    assert repr(s) == '7'
    assert no_cc_logging()


def test_18011709(t):
    """NEW_ONLY"""
    @strangled_method('__repr__', use=NEW_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.old = None
            self.new = Repr(lambda: 987)
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
