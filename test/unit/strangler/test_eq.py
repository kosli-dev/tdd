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
    cmp(use, True, True)
    cmp(use, False, False)


def diff(use):
    cmp(use, True, False)
    cmp(use, False, True)


def cmp(use, old, new):
    @strangled_method('__eq__', use=use)
    class Cmp:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = Eq(old)
            if use is not OLD_ONLY:
                self.new = Eq(new)

    c = Cmp()
    if use is OLD_ONLY:
        assert (c == c) is old
    elif use is NEW_ONLY:
        assert (c == c) is new
    elif old == new:
        assert (c == c) is old
    else:
        with pytest.raises(StrangledDifference) as exc:
            c == c
        check_strangler_exc(exc, "Cmp.__eq__", f"{old}", f"{new}")
    assert no_strangler_logging()


class Eq:
    def __init__(self, tf):
        self.tf = tf

    def __eq__(self, _other):
        return self.tf

