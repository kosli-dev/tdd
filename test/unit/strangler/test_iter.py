import pytest
from strangler import *
from .helpers import *


def test_011300():
    """OLD_ONLY"""
    @strangled_method('__iter__', use=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Iter([4, 6, 7])
            self.new = None
    d = Diff()

    assert ids(d) == [4, 6, 7]
    assert no_strangler_logging()


def test_011301():
    """NEW_TEST On Same"""
    @strangled_method('__iter__', use=NEW_TEST)
    class Same:
        def __init__(self):
            self.old = Iter([1, 6])
            self.new = Iter([1, 6])
    s = Same()

    assert ids(s) == [1, 6]
    assert no_strangler_logging()


def test_011302():
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


def test_011303():
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


def test_011304():
    """OLD_MAIN Same"""
    @strangled_method('__iter__', use=OLD_MAIN)
    class Same:
        def __init__(self):
            self.old = Iter([1, 60])
            self.new = Iter([1, 60])
    s = Same()

    assert ids(s) == [1, 60]
    assert no_strangler_logging()


def test_011305():
    """OLD_MAIN Different - same number of elements"""
    @strangled_method('__iter__', use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([10, 3])
            self.new = Iter([3, 10])
    d = Diff()

    assert ids(d) == [10, 3]
    check_log('[10, 3]', '[3, 10]')


def test_011306():
    """OLD_MAIN Different - different number of elements"""
    @strangled_method('__iter__', use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([1, 30, 9])
            self.new = Iter([1, 30])
    d = Diff()

    assert ids(d) == [1, 30, 9]
    check_log('[1, 30, 9]', '[1, 30]')


def test_011307():
    """NEW_MAIN Different"""
    @strangled_method('__iter__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([0])
            self.new = Iter([0, 3])
    d = Diff()

    assert ids(d) == [0, 3]
    check_log('[0]', '[0, 3]')


def test_011308():
    """NEW_MAIN Same"""
    @strangled_method('__iter__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([1, 9])
            self.new = Iter([1, 9])
    d = Diff()

    assert ids(d) == [1, 9]
    assert no_strangler_logging()


def test_011309():
    """NEW_ONLY"""
    @strangled_method('__iter__', use=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.old = None
            self.new = Iter([14, 26, 4])
    d = Diff()

    assert ids(d) == [14, 26, 4]
    assert no_strangler_logging()


def check_log(old, new):
    check_strangler_log('Diff', '__iter__', old, new)


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

    def __repr__(self):
        return f"{self.id}"

    def __eq__(self, other):
        return isinstance(other, II) and self.id == other.id

    def __lt__(self, other):
        return isinstance(other, II) and self.id < other.id
