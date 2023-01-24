import pytest
from strangler import *
from .helpers import *


def test_011600():
    """OLD_ONLY"""
    @strangled_property("p", getter=OLD_ONLY, setter=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Prop(42)
    d = Diff()

    assert d.p == 42
    assert no_strangler_logging()

    d.p = 11
    assert no_strangler_logging()
    assert d.p == 11


def test_011604():
    """OLD_MAIN"""
    @strangled_property("p", getter=OLD_MAIN, setter=OLD_MAIN)
    class Same:
        def __init__(self):
            self.old = Prop("ccc")
            self.new = Prop("ccc")
    s = Same()

    assert s.p == "ccc"
    assert no_strangler_logging()

    s.p = "anything"
    assert no_strangler_logging()
    assert s.p == "anything"

    @strangled_property("p", getter=OLD_MAIN, setter=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Prop("ccc")
            self.new = PropRaiser()
    d = Diff()

    with pytest.raises(StrangledDifference) as exc:
        d.p
    check_exc(exc, 'ccc', 'not-set')

    with pytest.raises(StrangledDifference) as exc:
        d.p = "anything"
    check_exc(exc, 'None', 'not-set')


def test_011606():
    """NEW_MAIN"""
    @strangled_property("p", getter=NEW_MAIN, setter=NEW_MAIN)
    class Same:
        def __init__(self):
            self.old = Prop(123)
            self.new = Prop(123)
    s = Same()

    assert s.p == 123
    assert no_strangler_logging()

    s.p = "foobar"
    assert no_strangler_logging()
    assert s.p == "foobar"

    @strangled_property("p", getter=NEW_MAIN, setter=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = PropRaiser()
            self.new = Prop(45)
    d = Diff()

    with pytest.raises(StrangledDifference) as exc:
        d.p
    check_exc(exc, 'not-set', '45')

    with pytest.raises(StrangledDifference) as exc:
        d.p = "anything"
    check_exc(exc, 'not-set', 'None')


def test_011608():
    """NEW_ONLY"""
    @strangled_property("p", getter=NEW_ONLY, setter=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.new = Prop(99)
    d = Diff()

    assert d.p == 99
    assert no_strangler_logging()

    d.p = "anything"
    assert no_strangler_logging()
    assert d.p == "anything"


def check_exc(exc, old, new):
    check_strangler_exc(exc, 'Diff', 'p', old, new)


class Prop:
    def __init__(self, v):
        self.v = v

    @property
    def p(self):
        return self.v

    @p.setter
    def p(self, value):
        self.v = value


class PropRaiser:

    @property
    def p(self):
        raise RuntimeError()

    @p.setter
    def p(self, _value):
        raise RuntimeError()
