import pytest
from strangler import *
from .helpers import *
import json


def test_d96700():
    """
    When use=NEW_TEST is True
    and NOT running unit-tests
    differences are NOT logged to a file.
    """
    @strangled_method("f", use=NEW_TEST)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 17)
            self.new = None

    d = Different()
    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        d.f()

    assert no_strangler_logging()


def test_d96701():
    """
    When use=NEW_TEST is True
    and running unit-tests
    a StrangledDifference is raised
    and differences are NOT logged to a file
    """
    @strangled_method("f", use=NEW_TEST)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 27)
            self.new = FuncF(lambda: 28)

    d = Different()
    with pytest.raises(StrangledDifference) as exc:
        d.f()

    check_exc_log(exc.value, 'Different', 'f', '27', '28')
    assert no_strangler_logging()


def test_d96702():
    """
    When use=NEW_TEST is not True
    a StrangledDifference is NOT raised
    differences are logged to a file.
    """
    @strangled_method("f", use=OLD_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 37)
            self.new = FuncF(lambda: 38)

    d = Different()
    d.f()

    assert strangler_log_file_exists()
    with open(strangler_log_filename(), "r") as file:
        log = json.loads(file.read())
        assert log["old"]["result"] == '37'
        assert log["new"]["result"] == '38'


def test_d96703():
    """
    Log's "is" key tells you whether old or new is primary.
    """
    @strangled_method("f", use=OLD_MAIN)
    @strangled_method("g", use=NEW_MAIN)
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 37)
            self.new = FuncF(lambda: 38)

    d = Different()
    d.f()
    log = get_strangler_log()
    assert log["old"]["is"] == 'primary'
    assert log["new"]["is"] == 'secondary'

    d.g()
    log = get_strangler_log()
    assert log["new"]["is"] == 'primary'
    assert log["old"]["is"] == 'secondary'


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
    d.f()
    log = get_strangler_log()
    expected = "\n".join([
        "new(p_res) == old(s_res) --> raised",
        '5, 4'
    ])
    assert log["summary"] == expected


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
    d.f()
    log = get_strangler_log()
    assert log["summary"] == "new(p_res) == old(s_res) --> False"


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
    with pytest.raises(NameError):
        d.f()
    log = get_strangler_log()
    expected = "\n".join([
        "type(new(p_exc)) != type(old(s_exc))",
        f"type(p_exc) is NameError",
        f"type(s_exc) is KeyError"
    ])
    assert log["summary"] == expected


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
    d.f()
    log = get_strangler_log()
    assert log["summary"] == "old did not raise, new raised"


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()

    def g(self):
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
