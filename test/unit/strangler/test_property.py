import pytest
from strangler import *
from .helpers import *


def test_011600(t):
    """OLD_ONLY"""
    @strangled_property("p", getter=OLD_ONLY, setter=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Prop(lambda: 42)
            self.new = None
    d = Diff()

    assert d.p == 42
    assert no_strangler_logging()

    d.p = 42
    assert no_strangler_logging()


def test_011601(t):
    """NEW_TEST On Same"""
    @strangled_property("p", getter=NEW_TEST, setter=NEW_TEST)
    class Same:
        def __init__(self):
            self.old = Prop(lambda: 5)
            self.new = Prop(lambda: 5)
    s = Same()

    assert s.p == 5
    assert no_strangler_logging()

    s.p = 5
    assert no_strangler_logging()


def test_011602(t):
    """NEW_TEST On Different"""
    @strangled_property("p", getter=NEW_TEST, setter=NEW_TEST)
    class Diff:
        def __init__(self):
            self.old = Prop(lambda: raiser())
            self.new = Prop(lambda: 6)

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d.p
    check_exc_log(exc.value, 'Diff', 'p', 'not-set', '6')
    assert no_strangler_logging()

    with pytest.raises(StrangledDifference) as exc:
        d.p = 42
    check_exc_log(exc.value, 'Diff', 'p', 'not-set', 'None')
    assert no_strangler_logging()


def test_011603(t):
    """NEW_TEST Off Different"""
    @strangled_property("p", getter=NEW_TEST, setter=NEW_TEST)
    class Diff:
        def __init__(self):
            self.old = Prop(lambda: 5)
            self.new = Prop(lambda: 6)
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert d.p == 5
    assert no_strangler_logging()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        d.p = 42
    assert no_strangler_logging()


def test_011604(t):
    """getter=OLD_MAIN Same"""
    @strangled_property("p", getter=OLD_MAIN, setter=OLD_MAIN)
    class Same:
        def __init__(self):
            self.old = Prop(lambda: "ccc")
            self.new = Prop(lambda: "ccc")
    s = Same()

    assert s.p == "ccc"
    assert no_strangler_logging()

    s.p = "anything"
    assert no_strangler_logging()


def test_011605(t):
    """getter=OLD_MAIN Different"""
    @strangled_property("p", getter=OLD_MAIN, setter=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Prop(lambda: "ccc")
            self.new = Prop(lambda: raiser())
    d = Diff()

    d.p
    check_log("Diff", 'p', 'ccc', 'not-set')

    d.p = "anything"
    check_log("Diff", 'p', 'None', 'not-set')


def test_011606(t):
    """NEW_MAIN Different"""
    @strangled_property("p", getter=NEW_MAIN, setter=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Prop(lambda: raiser())
            self.new = Prop(lambda: 45)
    d = Diff()

    assert d.p == 45
    check_log('Diff', 'p', 'not-set', '45')

    d.p = "anything"
    check_log('Diff', 'p', 'not-set', 'None')


def test_011607(t):
    """NEW_MAIN Same"""
    @strangled_property("p", getter=NEW_MAIN, setter=NEW_MAIN)
    class Same:
        def __init__(self):
            self.old = Prop(lambda: 123)
            self.new = Prop(lambda: 123)
    s = Same()

    assert s.p == 123
    assert no_strangler_logging()

    s.p = "anything"
    assert no_strangler_logging()


def test_011608(t):
    """NEW_ONLY"""
    @strangled_property("p", getter=NEW_ONLY, setter=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.old = None
            self.new = Prop(lambda: 99)
    d = Diff()

    assert d.p == 99
    assert no_strangler_logging()

    d.p = "anything"
    assert no_strangler_logging()

# - - - - - - - - - - - - - - - - - - - - - - -


class Prop:
    def __init__(self, v):
        self.v = v

    @property
    def p(self):
        return self.v()

    @p.setter
    def p(self, _value):
        self.v()
