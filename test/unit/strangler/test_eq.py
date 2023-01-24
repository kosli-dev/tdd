import pytest
from strangler import *
from .helpers import *


def test_011110():
    """OLD_ONLY"""
    @strangled_method('__eq__', use=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: True)

    d = Diff()
    assert d == d
    assert no_strangler_logging()


def test_011111():
    """OLD_MAIN"""
    @strangled_method('__eq__', use=OLD_MAIN)
    class Same:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: True)

    s = Same()
    assert s == s
    assert no_strangler_logging()

    @strangled_method('__eq__', use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: False)

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d == d
    check_exc(exc, True, False)
    assert no_strangler_logging()


def test_011114():
    """NEW_MAIN"""
    @strangled_method('__eq__', use=NEW_MAIN)
    class Same:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: True)

    s = Same()
    assert s == s
    assert no_strangler_logging()

    @strangled_method('__eq__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Eq(lambda: True)
            self.new = Eq(lambda: False)

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d == d
    check_exc(exc, True, False)
    assert no_strangler_logging()


def test_011118():
    """NEW_ONLY"""
    @strangled_method('__eq__', use=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.new = Eq(lambda: False)

    d = Diff()
    assert (d == d) is False
    assert no_strangler_logging()


def check_exc(exc, old, new):
    check_strangler_exc(exc, "Diff", '__eq__', f"{old}", f"{new}")


class Eq:
    def __init__(self, f):
        self.f = f

    def __eq__(self, _other):
        return self.f()

