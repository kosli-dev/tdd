import pytest
from strangler import *
from .helpers import *


def test_011200(t):
    """OLD_ONLY"""
    @strangled_method('__hash__', use=OLD_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.old = Hash(lambda: 8877)
            self.new = None
    d = Diff()

    assert hash(d) == 8877
    assert no_strangler_logging()


def test_011201(t):
    """NEW_TEST On Same"""
    @strangled_method('__hash__', use=NEW_TEST, kind="query")
    class Same:
        def __init__(self):
            self.old = Hash(lambda: 5)
            self.new = Hash(lambda: 5)
    s = Same()

    assert hash(s) == 5
    assert no_strangler_logging()


def test_011202(t):
    """NEW_TEST On Different"""
    @strangled_method('__hash__', use=NEW_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.old = Hash(lambda: 69)
            self.new = Hash(lambda: 56)
    d = Diff()

    with pytest.raises(StrangledDifference) as exc:
        hash(d)
    check_exc_log(exc.value, 'Diff', '__hash__', '69', '56')
    assert no_strangler_logging()


def test_011203(t):
    """NEW_TEST Off Different"""
    @strangled_method('__hash__', use=NEW_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.old = Hash(lambda: 23)
            self.new = Hash(lambda: raiser())
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert hash(d) == 23
    assert no_strangler_logging()


def test_011204(t):
    """OLD_MAIN Same"""
    @strangled_method('__hash__', use=OLD_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.old = Hash(lambda: 42)
            self.new = Hash(lambda: 42)
    s = Same()

    assert hash(s) == 42
    assert no_strangler_logging()


def test_011205(t):
    """OLD_MAIN Different"""
    @strangled_method('__hash__', use=OLD_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.old = Hash(lambda: 51)
            self.new = Hash(lambda: raiser())
    d = Diff()

    assert hash(d) == 51
    check_log('51', 'not-set')


def test_011206(t):
    """NEW_MAIN Different"""
    @strangled_method('__hash__', use=NEW_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.old = Hash(lambda: raiser())
            self.new = Hash(lambda: 45)
    d = Diff()

    assert hash(d) == 45
    check_log('not-set', '45')


def test_011207(t):
    """NEW_MAIN Same"""
    @strangled_method('__hash__', use=NEW_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.old = Hash(lambda: 7)
            self.new = Hash(lambda: 7)
    s = Same()

    assert hash(s) == 7
    assert no_strangler_logging()


def test_011208(t):
    """NEW_ONLY"""
    @strangled_method('__hash__', use=NEW_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.old = None
            self.new = Hash(lambda: 1122)
    d = Diff()

    assert hash(d) == 1122
    assert no_strangler_logging()


# - - - - - - - - - - - - - - - - - - - - - - -


def check_log(c, m):
    check_strangler_log('Diff', '__hash__', c, m)


class Hash:
    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return self.v()
