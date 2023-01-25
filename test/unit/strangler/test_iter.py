import pytest
from strangler import *
from .helpers import *


def test_011300():
    same(OLD_ONLY, [4, 5])
    diff(OLD_ONLY, [3], False)


def test_011304():
    same(OLD_MAIN, [1, 60])
    diff(OLD_MAIN, [10, 3], [3, 10])
    diff(OLD_MAIN, [1, 30, 9], [1, 30])


def test_011307():
    same(NEW_MAIN, [1, 9])
    diff(NEW_MAIN, [0, 3], [3, 0])
    diff(NEW_MAIN, [0], [0, 3])


def test_011309():
    same(NEW_ONLY, [5, 6])
    diff(NEW_ONLY, False, [7])


def same(use, nos):
    @strangled_method('__iter__', use=use)
    class Same:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = Iter(nos)
            if use is not OLD_ONLY:
                self.new = Iter(nos)

    s = Same()
    assert seq(s) == nos
    assert no_strangler_logging()


def diff(use, old, new):
    @strangled_method('__iter__', use=use)
    class Diff:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = Iter(old)
            if use is not OLD_ONLY:
                self.new = Iter(new)

    d = Diff()
    if use is OLD_ONLY:
        assert seq(d) == old
    elif use is NEW_ONLY:
        assert seq(d) == new
    else:
        with pytest.raises(StrangledDifference) as exc:
            seq(d)
        check_exc(exc, old, new)
    assert no_strangler_logging()


def check_exc(exc, old, new):
    check_strangler_exc(exc, "Diff.__iter__", f"{old}", f"{new}")


def seq(numbers):
    return [number for number in numbers]


class Iter:
    def __init__(self, seq):
        self.seq = [n for n in seq]
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index < len(self.seq):
            return self.seq[self.index]
        else:
            raise StopIteration
