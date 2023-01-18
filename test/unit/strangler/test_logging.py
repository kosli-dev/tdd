import pytest
from strangler import *
from .helpers import *
import json
import os
import shutil


def test_d96700(t):
    """
    When use=NEW_TEST is True
    and NOT running unit-tests
    differences are NOT logged to a file.
    """
    @strangled_method("f", use=NEW_TEST, kind="query")
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 17)
            self.new = FuncF(lambda: 18)

    d = Different()
    shutil.rmtree(STRANGLER_DEBUG_LOG_DIR)
    os.mkdir(STRANGLER_DEBUG_LOG_DIR)

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        d.f()
    assert get_cc_log() is None
    assert not os.path.exists(STRANGLER_DEBUG_LOG_QUERY_PATH)


def test_d96701(t):
    """
    When use=NEW_TEST is True
    and running unit-tests
    a StrangledDifference is raised
    and differences are NOT logged to a file
    """
    @strangled_method("f", use=NEW_TEST, kind="query")
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 27)
            self.new = FuncF(lambda: 28)

    d = Different()
    shutil.rmtree(STRANGLER_DEBUG_LOG_DIR)
    os.mkdir(STRANGLER_DEBUG_LOG_DIR)

    with pytest.raises(StrangledDifference) as exc:
        d.f()
    check_exc_log(exc.value, 'Different', 'f', '27', '28')
    assert get_cc_log() is None
    assert not os.path.exists(STRANGLER_DEBUG_LOG_QUERY_PATH)


def test_d96702(t):
    """
    When use=NEW_TEST is not True
    differences are logged to a file.
    """
    @strangled_method("f", use=OLD_MAIN, kind="query")
    class Different:
        def __init__(self):
            self.old = FuncF(lambda: 37)
            self.new = FuncF(lambda: 38)

    d = Different()
    shutil.rmtree(STRANGLER_DEBUG_LOG_DIR)
    os.mkdir(STRANGLER_DEBUG_LOG_DIR)

    d.f()
    assert os.path.exists(STRANGLER_DEBUG_LOG_QUERY_PATH)
    with open(STRANGLER_DEBUG_LOG_QUERY_PATH, "r") as file:
        log = json.loads(file.read())
        assert log["overwrite-db"]["result"] == '37'
        assert log["append-db"]["result"] == '38'


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
