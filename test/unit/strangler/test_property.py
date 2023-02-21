import pytest
from strangler import *
from .helpers import *


def test_011600():
    for use in switches():
        cmp(use, 45, 45)
        cmp(use, 23, 24)


def cmp(use, old, new):
    @strangled_property("p", getter=use, setter=None)
    class Cmp:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = Prop(old)
            if use is not OLD_ONLY:
                self.new = Prop(new)

    g = Cmp()
    if use is OLD_ONLY:
        assert g.p == old
    elif use is NEW_ONLY:
        assert g.p == new
    elif old == new:
        assert g.p == old
    else:
        with pytest.raises(StrangledDifference) as exc:
            g.p
        check_strangler_exc(exc, 'Cmp.p', f"{old}", f"{new}")
    assert no_strangler_logging()


def test_011604():
    """OLD_MAIN old returns, new raises"""
    @strangled_property("p", getter=OLD_MAIN, setter=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Prop(4)
            self.new = PropRaiser()

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d.p
    check_exc(exc, '4', "Raised()")

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d.p = "anything"
    check_exc(exc, 'None', "Raised()")


def test_011606():
    """NEW_MAIN old raises, new returns"""
    @strangled_property("p", getter=NEW_MAIN, setter=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = PropRaiser()
            self.new = Prop(45)

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d.p
    check_exc(exc, "Raised()", '45')

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        d.p = "anything"
    check_exc(exc, "Raised()", 'None')


def check_exc(exc, old, new):
    check_strangler_exc(exc, 'Diff.p', old, new)


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
