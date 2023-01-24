import pytest
from strangler import *
from .helpers import *


def test_011500():
    """OLD_ONLY"""
    @strangled_method("f", use=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Func(lambda: 11)

    d = Diff()
    assert d.f() == 11
    assert no_strangler_logging()


def test_011504():
    """OLD_MAIN"""
    @strangled_method("f", use=OLD_MAIN)
    class Same:
        def __init__(self):
            self.old = Func(lambda: 42)
            self.new = Func(lambda: 42)

    s = Same()
    assert s.f() == 42
    assert no_strangler_logging()

    @strangled_method("f", use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Func(lambda: 17)
            self.new = Func(lambda: 18)

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d.f()
    check_exc(exc, 17, 18)


def test_011506():
    """NEW_MAIN"""
    @strangled_method("f", use=NEW_MAIN)
    class Same:
        def __init__(self):
            self.old = Func(lambda: 33)
            self.new = Func(lambda: 33)

    s = Same()
    assert s.f() == 33
    assert no_strangler_logging()

    @strangled_method("f", use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Func(lambda: 17)
            self.new = Func(lambda: 18)

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d.f()
    check_exc(exc, 17, 18)


def test_011507():
    """NEW_ONLY"""
    @strangled_method("f", use=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.new = Func(lambda: "a")
    d = Diff()
    assert d.f() == "a"
    assert no_strangler_logging()


def check_exc(exc, old, new):
    check_strangler_exc(exc, 'Diff', 'f', f"{old}", f"{new}")


class Func:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
