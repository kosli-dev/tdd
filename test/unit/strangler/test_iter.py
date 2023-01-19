import pytest
from strangler import *
from .helpers import *


def test_011300(t):
    """OLD_ONLY"""
    @strangled_method('__iter__', use=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Iter([4, 6, 7])
            self.new = None
    d = Diff()

    assert ids(d) == [4, 6, 7]
    assert no_strangler_logging()


def test_011301(t):
    """NEW_TEST On Same"""
    @strangled_method('__iter__', use=NEW_TEST)
    class Same:
        def __init__(self):
            self.old = Iter([1, 6])
            self.new = Iter([1, 6])
    s = Same()

    assert ids(s) == [1, 6]
    assert no_strangler_logging()


def test_011302(t):
    """NEW_TEST On Different"""
    @strangled_method('__iter__', use=NEW_TEST)
    class Diff:
        def __init__(self):
            self.old = Iter([1, 6])
            self.new = Iter([0])
    d = Diff()

    with pytest.raises(StrangledDifference) as exc:
        ids(d)
    check_exc_log(exc.value, 'Diff', '__iter__', '[1, 6]', '[0]')
    assert no_strangler_logging()


def test_011303(t):
    """NEW_TEST Off Different"""
    @strangled_method('__iter__', use=NEW_TEST)
    class Diff:
        def __init__(self):
            self.old = Iter([5, 8])
            self.new = Iter([0])
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert ids(d) == [5, 8]
    assert no_strangler_logging()


def test_011304(t):
    """OLD_MAIN Same"""
    @strangled_method('__iter__', use=OLD_MAIN)
    class Same:
        def __init__(self):
            self.old = Iter([60, 1])
            self.new = Iter([1, 60])
    s = Same()

    assert ids(s) == [60, 1]
    assert no_strangler_logging()


def test_011305(t):
    """OLD_MAIN Different - same number of elements"""
    @strangled_method('__iter__', use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([10, 3])
            self.new = Iter([1, 10])
    d = Diff()

    assert ids(d) == [10, 3]
    check_log('[10, 3]', '[1, 10]')


def test_011306(t):
    """OLD_MAIN Different - different number of elements"""
    @strangled_method('__iter__', use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([30, 3, 9])
            self.new = Iter([1, 30])
    d = Diff()

    assert ids(d) == [30, 3, 9]
    check_log('[30, 3, 9]', '[1, 30]')


def test_011307(t):
    """NEW_MAIN Different"""
    @strangled_method('__iter__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([0, 9])
            self.new = Iter([5, 3])
    d = Diff()

    assert ids(d) == [5, 3]
    check_log('[0, 9]', '[5, 3]')


def test_011308(t):
    """NEW_MAIN Same"""
    @strangled_method('__iter__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([1, 9])
            self.new = Iter([1, 9])
    d = Diff()

    assert ids(d) == [1, 9]
    assert no_strangler_logging()


def test_011309(t):
    """NEW_ONLY"""
    @strangled_method('__iter__', use=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.old = None
            self.new = Iter([14, 26, 4])
    d = Diff()

    assert ids(d) == [14, 26, 4]
    assert no_strangler_logging()


# - - - - - - - - - - - - - - - - - - - - - - -

def check_log(c, m):
    check_strangler_log('Diff', '__iter__', c, m)


def ids(c):
    return [o.id for o in c]


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
        self.id = value


