import pytest
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_method
from .helpers import *
from helpers.unit.lib.scoped_env_var import ScopedEnvVar


def test_18011500(t):
    """OVERWRITE_ONLY"""
    @contract_checked_method("f", use=OVERWRITE_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Func(lambda: 11)
            self.append = None
    d = Diff()

    assert d.f() == 11
    assert no_cc_logging()


def test_18011501(t):
    """APPEND_TEST On Same"""
    @contract_checked_method("f", use=APPEND_TEST, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Func(lambda: 27)
            self.append = Func(lambda: 27)
    s = Same()

    assert s.f() == 27
    assert no_cc_logging()


def test_18011502(t):
    """APPEND_TEST On Different"""
    @contract_checked_method("f", use=APPEND_TEST, kind="command")
    class Diff:
        def __init__(self):
            self.overwrite = Func(lambda: 27)
            self.append = Func(lambda: raiser())
    d = Diff()

    with pytest.raises(ContractDifference) as exc:
        d.f()
    check_exc_log(exc.value, 'Diff', 'f', '27', 'not-set')
    assert no_cc_logging()


def test_18011503(t):
    """APPEND_TEST Off Different"""
    @contract_checked_method("f", use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Func(lambda: 27)
            self.append = Func(lambda: raiser())
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'NOT-unit'):
        assert d.f() == 27
    assert no_cc_logging()


def test_18011504(t):
    """OVERWRITE_MAIN Same"""
    @contract_checked_method("f", use=OVERWRITE_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Func(lambda: 42)
            self.append = Func(lambda: 42)
    s = Same()

    assert s.f() == 42
    assert get_cc_log() is None


def test_18011505(t):
    """OVERWRITE_MAIN Different"""
    @contract_checked_method("f", use=OVERWRITE_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Func(lambda: 17)
            self.append = Func(lambda: 18)
    d = Diff()

    assert d.f() == 17
    check_cm_log('17', '18')


def test_18011506(t):
    """APPEND_MAIN Different"""
    @contract_checked_method("f", use=APPEND_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Func(lambda: 17)
            self.append = Func(lambda: 18)
    d = Diff()

    assert d.f() == 18
    check_cm_log('17', '18')


def test_18011507(t):
    """APPEND_ONLY"""
    @contract_checked_method("f", use=APPEND_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = None
            self.append = Func(lambda: "a")
    d = Diff()

    assert d.f() == "a"
    assert no_cc_logging()


# - - - - - - - - - - - - - - - - - - - - - - -


def check_cm_log(c, m):
    check_cc_log('Diff', 'f', c, m)


class Func:
    def __init__(self, v):
        self.v = v

    def f(self):
        return self.v()

    def _reset(self):
        pass
