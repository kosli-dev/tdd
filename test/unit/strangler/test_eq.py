import pytest
from strangler import *
from .helpers import *


def test_011110(t):
    """OLD_ONLY"""
    @strangled_method('__eq__', use=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = None
    d = Diff()

    assert d == d
    assert no_strangler_logging()


def test_011111(t):
    """NEW_TEST On Same"""
    @strangled_method('__eq__', use=NEW_TEST)
    class Same:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: True)
    s = Same()

    assert s == s
    assert no_strangler_logging()


def test_011112(t):
    """NEW_TEST On Different"""
    @strangled_method('__eq__', use=NEW_TEST)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: False)
    d = Diff()

    with pytest.raises(StrangledDifference) as exc:
        d == d
    check_exc_log(exc.value, "Diff", '__eq__', 'True', 'False')
    assert no_strangler_logging()


def test_011113(t):
    """NEW_TEST Off Different"""
    @strangled_method('__eq__', use=NEW_TEST)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: False)
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert d == d
    assert no_strangler_logging()


def test_011114(t):
    """NEW_MAIN Same"""
    @strangled_method('__eq__', use=NEW_MAIN)
    class Same:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: True)
    s = Same()

    assert s == s
    assert no_strangler_logging()


def test_011115(t):
    """NEW_MAIN Different"""
    @strangled_method('__eq__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: False)
    d = Diff()

    assert d != d
    check_log('True', 'False')


def test_011116(t):
    """NEW_MAIN Different"""
    @strangled_method('__eq__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: False)
    d = Diff()

    assert d != d
    check_log('True', 'False')


def test_011117(t):
    """NEW_MAIN Same"""
    @strangled_method('__eq__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: False)
            self.new = Eq(lambda: False)
    d = Diff()

    assert d != d
    assert no_strangler_logging()


def test_011118(t):
    """NEW_ONLY"""
    @strangled_method('__eq__', use=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.old = None
            self.new = Eq(lambda: True)
    d = Diff()

    assert d == d
    assert no_strangler_logging()

# - - - - - - - - - - - - - - - - - - - - - - -


def check_log(old, new):
    check_strangler_log('Diff', '__eq__', old, new)


class Eq:
    def __init__(self, f):
        self.f = f

    def __eq__(self, _other):
        return self.f()

