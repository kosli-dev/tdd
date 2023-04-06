import pytest
from strangler import *
from .helpers import *
import json


def test_d96700():
    """
    When NOT running unit-tests
    a difference is NOT raised
    but is logged instead.
    """
    @strangled_method("f", use=OLD_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 17)
            self.new = FuncF(lambda: 18)

    d = Different()
    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert d.f() == 17

    assert strangler_log_file_exists()
    with open(strangler_log_filename(), "r") as file:
        log = json.loads(file.read())
        assert log["old"]["result"] == '17'
        assert log["new"]["result"] == '18'


def test_d96701():
    """
    Handle repr() raising an exception
    when producing diff report
    """
    class ReprRaiser:
        def f(self):
            return self

        def __repr__(self):
            raise RuntimeError("X")

    @strangled_method("f", use=OLD_MAIN)
    class Different:
        def __init__(self):
            self.old = ReprRaiser()
            self.new = ReprRaiser()

    d = Different()
    with pytest.raises(StrangledDifference) as exc:
        d.f()


def test_d96703():
    """
    Log's "is" key tells you whether
    old or new is primary.
    """
    @strangled_method("f", use=OLD_MAIN)
    @strangled_method("g", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 37)
            self.new = FuncF(lambda: 38)

    d = Different()
    with pytest.raises(StrangledDifference) as exc:
        d.f()
    diff = exc.value.diff
    assert diff["old"]["is"] == 'primary'
    assert diff["new"]["is"] == 'secondary'


def test_d96704():
    """
    Log's "summary" key tells you
    when the inner == comparison raises
    """
    @strangled_method("f", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = RaisingEq(4)
            self.new = RaisingEq(5)

    d = Different()
    with pytest.raises(StrangledDifference) as exc:
        d.f()
    diff = exc.value.diff
    expected = [
        "old['result'] == new['result'] --> raised!",
        '4, 5'
    ]
    assert diff["summary"] == expected


def test_d96705():
    """
    Log's "summary" key tells you
    when the inner == comparison returns False
    """
    @strangled_method("f", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 4)
            self.new = FuncF(lambda: 5)

    d = Different()
    with pytest.raises(StrangledDifference) as exc:
        d.f()
    diff = exc.value.diff
    assert diff["summary"] == "old['result'] == new['result'] --> False"


def test_d96706():
    """
    Log's "summary" key tells you
    when Old/New raise different exceptions
    """
    @strangled_method("f", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: raiser(KeyError("x")))
            self.new = FuncF(lambda: raiser(NameError("y")))

    d = Different()
    with pytest.raises(StrangledDifference) as exc:
        d.f()
    diff = exc.value.diff
    expected = "\n".join([
        "Different exception types",
        f"type(old['exception']) is KeyError",
        f"type(new['exception']) is NameError"
    ])
    assert diff["summary"] == expected


def test_d96707():
    """
    Log's "summary" key tells you
    when one of Old/New raises and the other doesn't
    """
    @strangled_method("f", use=OLD_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 42)
            self.new = FuncF(lambda: raiser(NameError("y")))

    d = Different()
    with pytest.raises(StrangledDifference) as exc:
        d.f()
    diff = exc.value.diff
    assert diff["summary"] == "old did not raise, new raised"


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()


class RaisingEq:

    def __init__(self, n):
        self.n = n

    def f(self):
        return RaiserEq(self.n)


class RaiserEq:

    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        raise RuntimeError(f"{self.n}, {other.n}")
