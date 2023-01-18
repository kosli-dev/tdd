import pytest
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_method
from .helpers import *
from helpers.unit.lib.scoped_env_var import ScopedEnvVar
import json
import os
import shutil


def test_0bd96700(t):
    """
    When use=APPEND_TEST is True
    and NOT running unit-tests
    differences are NOT logged to a file.
    """
    @contract_checked_method("f", use=APPEND_TEST, kind="query")
    class Different:
        def __init__(self):
            self.overwrite = FuncF(lambda: 17)
            self.append = FuncF(lambda: 18)

    d = Different()
    shutil.rmtree(APPEND_CONTRACT_DEBUG_LOG_DIR)
    os.mkdir(APPEND_CONTRACT_DEBUG_LOG_DIR)

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        d.f()
    assert get_cc_log() is None
    assert not os.path.exists(APPEND_CONTRACT_DEBUG_LOG_QUERY_PATH)


def test_0bd96701(t):
    """
    When use=APPEND_TEST is True
    and running unit-tests
    a ContractDifferenceTestingError is raised
    and differences are NOT logged to a file
    """
    @contract_checked_method("f", use=APPEND_TEST, kind="query")
    class Different:
        def __init__(self):
            self.overwrite = FuncF(lambda: 27)
            self.append = FuncF(lambda: 28)

    d = Different()
    shutil.rmtree(APPEND_CONTRACT_DEBUG_LOG_DIR)
    os.mkdir(APPEND_CONTRACT_DEBUG_LOG_DIR)

    with pytest.raises(ContractDifference) as exc:
        d.f()
    check_exc_log(exc.value, 'Different', 'f', '27', '28')
    assert get_cc_log() is None
    assert not os.path.exists(APPEND_CONTRACT_DEBUG_LOG_QUERY_PATH)


def test_0bd96702(t):
    """
    When use=APPEND_TEST is not True
    differences are logged to a file.
    """
    @contract_checked_method("f", use=OVERWRITE_MAIN, kind="query")
    class Different:
        def __init__(self):
            self.overwrite = FuncF(lambda: 37)
            self.append = FuncF(lambda: 38)

    d = Different()
    shutil.rmtree(APPEND_CONTRACT_DEBUG_LOG_DIR)
    os.mkdir(APPEND_CONTRACT_DEBUG_LOG_DIR)

    d.f()
    assert os.path.exists(APPEND_CONTRACT_DEBUG_LOG_QUERY_PATH)
    with open(APPEND_CONTRACT_DEBUG_LOG_QUERY_PATH, "r") as file:
        log = json.loads(file.read())
        assert log["overwrite-db"]["result"] == '37'
        assert log["append-db"]["result"] == '38'


class FuncF:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()
