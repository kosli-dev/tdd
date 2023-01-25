import pytest
from strangler import *
from .helpers import *


def test_011110():
    same(OLD_ONLY)
    diff(OLD_ONLY)


def test_011111():
    same(OLD_MAIN)
    diff(OLD_MAIN)


def test_011114():
    same(NEW_MAIN)
    diff(NEW_MAIN)


def test_011118():
    same(NEW_ONLY)
    diff(NEW_ONLY)


def same(use):
    @strangled_method('__eq__', use=use)
    class Same:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = Eq(True)
            if use is not OLD_ONLY:
                self.new = Eq(True)

    s = Same()
    assert s == s
    assert no_strangler_logging()


def diff(use):
    @strangled_method('__eq__', use=use)
    class Diff:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = Eq(True)
            if use is not OLD_ONLY:
                self.new = Eq(False)

    d = Diff()
    if use is OLD_ONLY:
        assert (d == d) is True
    elif use is NEW_ONLY:
        assert (d == d) is False
    else:
        with pytest.raises(StrangledDifference) as exc:
            d == d
        check_strangler_exc(exc, "Diff.__eq__", "True", "False")
    assert no_strangler_logging()


class Eq:
    def __init__(self, tf):
        self.tf = tf

    def __eq__(self, _other):
        return self.tf

