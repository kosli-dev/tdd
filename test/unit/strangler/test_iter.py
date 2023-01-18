import pytest
from lib.contract_check import *
from lib.contract_check_decorators import contract_checked_method
from .helpers import *
from helpers.unit.lib.scoped_env_var import ScopedEnvVar


def test_18011300(t):
    """OVERWRITE_ONLY"""
    @contract_checked_method('__iter__', use=OVERWRITE_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Iter([4, 6, 7])
            self.append = None
    d = Diff()

    assert ids(d) == [4, 6, 7]
    assert no_cc_logging()


def test_18011301(t):
    """APPEND_TEST On Same"""
    @contract_checked_method('__iter__', use=APPEND_TEST, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Iter([1, 6])
            self.append = Iter([1, 6])
    s = Same()

    assert ids(s) == [1, 6]
    assert no_cc_logging()


def test_18011302(t):
    """APPEND_TEST On Different"""
    @contract_checked_method('__iter__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Iter([1, 6])
            self.append = Iter([0])
    d = Diff()

    with pytest.raises(ContractDifference) as exc:
        ids(d)
    check_exc_log(exc.value, 'Diff', '__iter__', '[1, 6]', '[0]')
    assert no_cc_logging()


def test_18011303(t):
    """APPEND_TEST Off Different"""
    @contract_checked_method('__iter__', use=APPEND_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Iter([5, 8])
            self.append = Iter([0])
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert ids(d) == [5, 8]
    assert no_cc_logging()


def test_18011304(t):
    """OVERWRITE_MAIN Same"""
    @contract_checked_method('__iter__', use=OVERWRITE_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.overwrite = Iter([60, 1])
            self.append = Iter([1, 60])
    s = Same()

    assert ids(s) == [60, 1]
    assert no_cc_logging()


def test_18011305(t):
    """OVERWRITE_MAIN Different - same number of elements"""
    @contract_checked_method('__iter__', use=OVERWRITE_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Iter([10, 3])
            self.append = Iter([1, 10])
    d = Diff()

    assert ids(d) == [10, 3]
    check_cm_log('[10, 3]', '[1, 10]')


def test_18011306(t):
    """OVERWRITE_MAIN Different - different number of elements"""
    @contract_checked_method('__iter__', use=OVERWRITE_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Iter([30, 3, 9])
            self.append = Iter([1, 30])
    d = Diff()

    assert ids(d) == [30, 3, 9]
    check_cm_log('[30, 3, 9]', '[1, 30]')


def test_18011307(t):
    """APPEND_MAIN Different"""
    @contract_checked_method('__iter__', use=APPEND_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Iter([0, 9])
            self.append = Iter([5, 3])
    d = Diff()

    assert ids(d) == [5, 3]
    check_cm_log('[0, 9]', '[5, 3]')


def test_18011308(t):
    """APPEND_MAIN Same"""
    @contract_checked_method('__iter__', use=APPEND_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = Iter([1, 9])
            self.append = Iter([1, 9])
    d = Diff()

    assert ids(d) == [1, 9]
    assert no_cc_logging()


def test_18011309(t):
    """APPEND_ONLY"""
    @contract_checked_method('__iter__', use=APPEND_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.overwrite = None
            self.append = Iter([14, 26, 4])
    d = Diff()

    assert ids(d) == [14, 26, 4]
    assert no_cc_logging()


# - - - - - - - - - - - - - - - - - - - - - - -

def check_cm_log(c, m):
    check_cc_log('Diff', '__iter__', c, m)


def ids(c):
    return [o.inner_id for o in c]


class Iter:
    def __init__(self, array):
        self.array = [II(n) for n in array]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.array):
            result = self.array[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


class II:
    def __init__(self, value):
        self.inner_id = value


