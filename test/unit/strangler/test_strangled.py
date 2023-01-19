import pytest
from strangler import *
from .helpers import *


def test_bba0d0():
    """
    When old or new is primary and it raises
    the exception is propagated.
    """
    @strangled_method("f", use=OLD_MAIN)
    class OldRaiser:
        def __init__(self):
            self.old = FuncF(lambda: raiser())
            self.new = None

    o = OldRaiser()
    with pytest.raises(RuntimeError):
        o.f()

    @strangled_method("f", use=NEW_MAIN)
    class NewRaiser:
        def __init__(self):
            self.old = None
            self.new = FuncF(lambda: raiser())

    r = NewRaiser()
    with pytest.raises(RuntimeError):
        r.f()


def test_bba0d1():
    """
    When old_is_on() and there is no attribute called old
    then AttributeError is raised.
    """
    @strangled_method("f", use=OLD_MAIN)
    class Different:
        def __init__(self):
            # self.old = FuncF(lambda: 42)
            self.new = FuncF(lambda: 43)

    d = Different()
    with pytest.raises(AttributeError):
        d.f()


def test_bba0d2():
    """
    When new_is_on() and there is no attribute called new
    then AttributeError is raised.
    """
    @strangled_method("f", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 42)
            # self.new = FuncF(lambda: 43)

    d = Different()
    with pytest.raises(AttributeError):
        d.f()


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
