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


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
