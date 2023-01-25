import pytest
from strangler import *
from .helpers import *


def test_011300():
    """OLD_ONLY"""
    @strangled_method('__iter__', use=OLD_ONLY)
    class Diff:
        def __init__(self):
            self.old = Iter([4, 6, 7])

    d = Diff()
    assert ids(d) == [4, 6, 7]
    assert no_strangler_logging()


def test_011304():
    """OLD_MAIN"""
    @strangled_method('__iter__', use=OLD_MAIN)
    class Same:
        def __init__(self):
            self.old = Iter([1, 60])
            self.new = Iter([1, 60])

    s = Same()
    assert ids(s) == [1, 60]
    assert no_strangler_logging()

    @strangled_method('__iter__', use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([10, 3])
            self.new = Iter([3, 10])

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        ids(d)
    check_exc(exc, [10, 3], [3, 10])
    assert no_strangler_logging()

    @strangled_method('__iter__', use=OLD_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([1, 30, 9])
            self.new = Iter([1, 30])

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        ids(d)
    check_exc(exc, [1, 30, 9], [1, 30])
    assert no_strangler_logging()


def test_011307():
    """NEW_MAIN"""
    @strangled_method('__iter__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([1, 9])
            self.new = Iter([1, 9])

    d = Diff()
    assert ids(d) == [1, 9]
    assert no_strangler_logging()

    @strangled_method('__iter__', use=NEW_MAIN)
    class Diff:
        def __init__(self):
            self.old = Iter([0])
            self.new = Iter([0, 3])

    d = Diff()
    with pytest.raises(StrangledDifference) as exc:
        ids(d)
    check_exc(exc, [0], [0, 3])
    assert no_strangler_logging()


def test_011309():
    """NEW_ONLY"""
    @strangled_method('__iter__', use=NEW_ONLY)
    class Diff:
        def __init__(self):
            self.new = Iter([14, 26, 4])

    d = Diff()
    assert ids(d) == [14, 26, 4]
    assert no_strangler_logging()


def check_exc(exc, old, new):
    check_strangler_exc(exc, "Diff.__iter__", f"{old}", f"{new}")


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
