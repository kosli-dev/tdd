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
    @strangled_method("f", use=use)
    class Same:
        def __init__(self):
            self.old = Func(lambda: 42)
            self.new = Func(lambda: 42)

    s = Same()
    assert s.f() == 42
    assert no_strangler_logging()


def diff(use):
    @strangled_method("f", use=use)
    class Diff:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = Func(lambda: 17)
            if use is not OLD_ONLY:
                self.new = Func(lambda: 18)

    d = Diff()
    if use is OLD_ONLY:
        assert d.f() == 17
    elif use is NEW_ONLY:
        assert d.f() == 18
    else:
        with pytest.raises(StrangledDifference) as exc:
            d.f()
        check_strangler_exc(exc, 'Diff.f', "17", "18")
    assert no_strangler_logging()


class Func:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
