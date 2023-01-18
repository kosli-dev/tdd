import pytest
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_method
from .helpers import *
from helpers.unit.lib.scoped_env_var import ScopedEnvVar


def test_18011400(t):
    """OVERWRITE_ONLY"""
    @contract_checked_method('__len__', use=OVERWRITE_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Len(lambda: 8742)
            self.append = None
    d = Diff()

    assert len(d) == 8742
    assert no_cc_logging()


def test_18011401(t):
    """APPEND_TEST On Same"""
    @contract_checked_method('__len__', use=APPEND_TEST, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Len(lambda: 5)
            self.append = Len(lambda: 5)
    s = Same()

    assert len(s) == 5
    assert no_cc_logging()


def test_18011402(t):
    """APPEND_TEST On Different"""
    @contract_checked_method('__len__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Len(lambda: 69)
            self.append = Len(lambda: 56)
    d = Diff()

    with pytest.raises(ContractDifference) as exc:
        len(d)
    check_exc_log(exc.value, 'Diff', '__len__', '69', '56')
    assert no_cc_logging()


def test_18011403(t):
    """APPEND_TEST Off Different"""
    @contract_checked_method('__len__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Len(lambda: 23)
            self.append = Len(lambda: raiser())
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert len(d) == 23
    assert no_cc_logging()


def test_18011404(t):
    """OVERWRITE_MAIN Same"""
    @contract_checked_method('__len__', use=OVERWRITE_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Len(lambda: 4228)
            self.append = Len(lambda: 4228)
    s = Same()

    assert len(s) == 4228
    assert no_cc_logging()


def test_18011405(t):
    """OVERWRITE_MAIN Different"""
    @contract_checked_method('__len__', use=OVERWRITE_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Len(lambda: 517)
            self.append = Len(lambda: 518)
    d = Diff()

    assert len(d) == 517
    check_cm_log('517', '518')


def test_18011407(t):
    """APPEND_MAIN Different"""
    @contract_checked_method('__len__', use=APPEND_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Len(lambda: raiser())
            self.append = Len(lambda: 45)
    d = Diff()

    assert len(d) == 45
    check_cm_log('not-set', '45')


def test_18011408(t):
    """APPEND_MAIN Same"""
    @contract_checked_method('__len__', use=APPEND_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Len(lambda: 7)
            self.append = Len(lambda: 7)
    s = Same()

    assert len(s) == 7
    assert no_cc_logging()


def test_18011409(t):
    """APPEND_ONLY"""
    @contract_checked_method('__len__', use=APPEND_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = None
            self.append = Len(lambda: 1212)
    d = Diff()

    assert len(d) == 1212
    assert no_cc_logging()

# - - - - - - - - - - - - - - - - - - - - - - -


def check_cm_log(c, m):
    check_cc_log('Diff', '__len__', c, m)


class Len:
    def __init__(self, v):
        self.v = v

    def __len__(self):
        return self.v()
