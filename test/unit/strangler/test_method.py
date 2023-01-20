import pytest
from strangler import *
from .helpers import *


def test_011500():
    """OLD_ONLY"""
    @strangled_method("f", use=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Func(lambda: 11)
            self.new = None
    d = Diff()

    assert d.f() == 11
    assert no_strangler_logging()


def test_011501():
    """NEW_TEST On Same"""
    @strangled_method("f", use=NEW_TEST)
    class Same:
        def __init__(self):
            self.old = Func(lambda: 27)
            self.new = Func(lambda: 27)
    s = Same()

    assert s.f() == 27
    assert no_strangler_logging()


def test_011502():
    """NEW_TEST On Different"""
    @strangled_method("f", use=NEW_TEST)
    class Diff:
        def __init__(self):
            self.old = Func(lambda: 27)
            self.new = Func(lambda: raiser())
    d = Diff()

    with pytest.raises(StrangledDifference) as exc:
        d.f()
    check_exc_log(exc.value, 'Diff', 'f', '27', 'not-set')
    assert no_strangler_logging()


def test_011503():
    """NEW_TEST Off Different"""
    @strangled_method("f", use=NEW_TEST)
    class Diff:
        def __init__(self):
            self.old = Func(lambda: 27)
            self.new = None
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'NOT-unit'):
        assert d.f() == 27
    assert no_strangler_logging()


def test_011504():
    """OLD_MAIN Same"""
    @strangled_method("f", use=OLD_MAIN)
    class Same:
        def __init__(self):
            self.old = Func(lambda: 42)
            self.new = Func(lambda: 42)
    s = Same()

    assert s.f() == 42
    assert no_strangler_logging()


def test_011505():
    """OLD_MAIN Different"""
    @strangled_method("f", use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Func(lambda: 17)
            self.new = Func(lambda: 18)
    d = Diff()

    assert d.f() == 17
    check_log('17', '18')


def test_011506():
    """NEW_MAIN Different"""
    @strangled_method("f", use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Func(lambda: 17)
            self.new = Func(lambda: 18)
    d = Diff()

    assert d.f() == 18
    check_log('17', '18')


def test_011507():
    """NEW_ONLY"""
    @strangled_method("f", use=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.old = None
            self.new = Func(lambda: "a")
    d = Diff()

    assert d.f() == "a"
    assert no_strangler_logging()


def check_log(old, new):
    check_strangler_log('Diff', 'f', old, new)


class Func:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
