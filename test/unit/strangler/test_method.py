import pytest
from strangler import *
from .helpers import *


def test_011500():
    same(OLD_ONLY)
    diff(OLD_ONLY)


def test_011504():
    same(OLD_MAIN)
    diff(OLD_MAIN)


def test_011506():
    same(NEW_MAIN)
    diff(NEW_MAIN)


def test_011507():
    same(NEW_ONLY)
    diff(NEW_ONLY)


def same(use):
    cmp(use, 45, 45)


def diff(use):
    cmp(use, 23, 24)


def cmp(use, old, new):
    @strangled_method("f", use=use)
    class Cmp:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = Func(old)
            if use is not OLD_ONLY:
                self.new = Func(new)

    c = Cmp()
    if use is OLD_ONLY:
        assert c.f() == old
    elif use is NEW_ONLY:
        assert c.f() == new
    elif old == new:
        assert c.f() == old
    else:
        with pytest.raises(StrangledDifference) as exc:
            c.f()
        check_strangler_exc(exc, 'Cmp.f', f"{old}", f"{new}")
    assert no_strangler_logging()


class Func:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v
