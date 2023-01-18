import pytest
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_property
from .helpers import *
from helpers.unit.lib.scoped_env_var import ScopedEnvVar


def test_18011600(t):
    """OVERWRITE_ONLY"""
    @contract_checked_property("p", getter=OVERWRITE_ONLY, setter=OVERWRITE_ONLY)
    class Diff:
        def __init__(self):
            self.overwrite = Prop(lambda: 42)
            self.append = None
    d = Diff()

    assert d.p == 42
    assert no_cc_logging()

    d.p = 42
    assert no_cc_logging()


def test_18011601(t):
    """APPEND_TEST On Same"""
    @contract_checked_property("p", getter=APPEND_TEST, setter=APPEND_TEST)
    class Same:
        def __init__(self):
            self.overwrite = Prop(lambda: 5)
            self.append = Prop(lambda: 5)
    s = Same()

    assert s.p == 5
    assert no_cc_logging()

    s.p = 5
    assert no_cc_logging()


def test_18011602(t):
    """APPEND_TEST On Different"""
    @contract_checked_property("p", getter=APPEND_TEST, setter=APPEND_TEST)
    class Diff:
        def __init__(self):
            self.overwrite = Prop(lambda: raiser())
            self.append = Prop(lambda: 6)

    d = Diff()
    with pytest.raises(ContractDifference) as exc:
        d.p
    check_exc_log(exc.value, 'Diff', 'p', 'not-set', '6')
    assert no_cc_logging()

    with pytest.raises(ContractDifference) as exc:
        d.p = 42
    check_exc_log(exc.value, 'Diff', 'p', 'not-set', 'None')
    assert no_cc_logging()


def test_18011603(t):
    """APPEND_TEST Off Different"""
    @contract_checked_property("p", getter=APPEND_TEST, setter=APPEND_TEST)
    class Diff:
        def __init__(self):
            self.overwrite = Prop(lambda: 5)
            self.append = Prop(lambda: 6)
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert d.p == 5
    assert no_cc_logging()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        d.p = 42
    assert no_cc_logging()


def test_18011604(t):
    """getter=OVERWRITE_MAIN Same"""
    @contract_checked_property("p", getter=OVERWRITE_MAIN, setter=OVERWRITE_MAIN)
    class Same:
        def __init__(self):
            self.overwrite = Prop(lambda: "ccc")
            self.append = Prop(lambda: "ccc")
    s = Same()

    assert s.p == "ccc"
    assert no_cc_logging()

    s.p = "anything"
    assert no_cc_logging()


def test_18011605(t):
    """getter=OVERWRITE_MAIN Different"""
    @contract_checked_property("p", getter=OVERWRITE_MAIN, setter=OVERWRITE_MAIN)
    class Diff:
        def __init__(self):
            self.overwrite = Prop(lambda: "ccc")
            self.append = Prop(lambda: raiser())
    d = Diff()

    d.p
    check_cc_log("Diff", 'p', 'ccc', 'not-set')

    d.p = "anything"
    check_cc_log("Diff", 'p', 'None', 'not-set')


def test_18011606(t):
    """APPEND_MAIN Different"""
    @contract_checked_property("p", getter=APPEND_MAIN, setter=APPEND_MAIN)
    class Diff:
        def __init__(self):
            self.overwrite = Prop(lambda: raiser())
            self.append = Prop(lambda: 45)
    d = Diff()

    assert d.p == 45
    check_cc_log('Diff', 'p', 'not-set', '45')

    d.p = "anything"
    check_cc_log('Diff', 'p', 'not-set', 'None')


def test_18011607(t):
    """APPEND_MAIN Same"""
    @contract_checked_property("p", getter=APPEND_MAIN, setter=APPEND_MAIN)
    class Same:
        def __init__(self):
            self.overwrite = Prop(lambda: 123)
            self.append = Prop(lambda: 123)
    s = Same()

    assert s.p == 123
    assert no_cc_logging()

    s.p = "anything"
    assert no_cc_logging()


def test_18011608(t):
    """APPEND_ONLY"""
    @contract_checked_property("p", getter=APPEND_ONLY, setter=APPEND_ONLY)
    class Diff:
        def __init__(self):
            self.overwrite = None
            self.append = Prop(lambda: 99)
    d = Diff()

    assert d.p == 99
    assert no_cc_logging()

    d.p = "anything"
    assert no_cc_logging()

# - - - - - - - - - - - - - - - - - - - - - - -


class Prop:
    def __init__(self, v):
        self.v = v

    @property
    def p(self):
        return self.v()

    @p.setter
    def p(self, _value):
        self.v()

    def _reset(self):
        pass
