import pytest
from strangler import *
from .helpers import *


def test_bba0d0():
    """
    When old or new is primary and it raises
    the exception is propagated.
    """
    @strangled_method("f", use=OLD_ONLY)
    class OldRaiser:
        def __init__(self):
            self.old = FuncF(lambda: raiser(KeyError('x')))
            self.new = None

    o = OldRaiser()
    with pytest.raises(KeyError) as exc:
        o.f()
    assert str(exc.value) == "'x'"

    @strangled_method("f", use=NEW_ONLY)
    class NewRaiser:
        def __init__(self):
            self.old = None
            self.new = FuncF(lambda: raiser(BufferError('shine')))

    r = NewRaiser()
    with pytest.raises(BufferError) as exc:
        r.f()
    assert str(exc.value) == "shine"


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


def test_bba0d3():
    """
    StrangledException __str__ prints indented json
    """
    @strangled_method("f", use=NEW_TEST)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 42)
            self.new = FuncF(lambda: 43)

    d = Different()
    with pytest.raises(StrangledDifference) as exc:
        d.f()
    s = f"{exc.value}"
    info = json.loads(s)
    assert info["old-info"] == {
        "result": '42',
        "exception": ["None", ""]
    }
    assert info["new-info"] == {
        "result": '43',
        "exception": ["None", ""]
    }


def test_bba0d4():
    """
    When neither Old nor New raise
    but the (p_res == s_res) comparison raises an exception
    then map that exception to a custom StranglingException.
    """
    @strangled_method("f", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: EqRaiser(42))
            self.new = FuncF(lambda: EqRaiser(42))

    d = Different()
    with pytest.raises(StranglingException) as exc:
        d.f()

    assert str(exc.value) == "p_res == s_res"


def test_bba0d5():
    """
    When Old and New both raise
    but the exceptions are of different types
    then raise a custom StranglingException.
    """
    @strangled_method("f", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: raiser(NameError()))
            self.new = FuncF(lambda: raiser(RuntimeError()))

    d = Different()
    with pytest.raises(StranglingException) as exc:
        d.f()

    expected = "\n".join([
        "type(p_exc) is RuntimeError",
        "type(s_exc) is NameError"
    ])
    assert str(exc.value) == expected


def test_bba0d6():
    """
    When Old and New both raise
    and the exceptions are of the same type
    then don't raise a custom StranglingException
    then do propagate the raised exception based on use=
    """
    @strangled_method("f", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: raiser(NameError("old")))
            self.new = FuncF(lambda: raiser(NameError("new")))

    d = Different()
    with pytest.raises(NameError) as exc:
        d.f()

    assert str(exc.value) == "new"


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()


class EqRaiser:
    def __init__(self, v):
        self.v = v

    def __eq__(self, _other):
        raise RuntimeError("oops")
