import pytest
from strangler import *
from .helpers import *


def test_011300():
    same(OLD_ONLY)
    diff(OLD_ONLY, [], False)
    diff(OLD_ONLY, [3], False)


def test_011304():
    same(OLD_MAIN)
    diff(OLD_MAIN, [10, 3], [3, 10])
    diff(OLD_MAIN, [1, 30, 9], [1, 30])


def test_011307():
    same(NEW_MAIN)
    diff(NEW_MAIN, [0, 3], [3, 0])
    diff(NEW_MAIN, [0], [0, 3])


def test_011309():
    same(NEW_ONLY)
    diff(NEW_ONLY, False, [])
    diff(NEW_ONLY, False, [7])


def same(use):
    cmp(use, [], [])
    cmp(use, [1], [1])
    cmp(use, [1, 2], [1, 2])


def diff(use, old, new):
    cmp(use, old, new)


def cmp(use, old, new):
    @strangled_method('__iter__', use=use)
    class Cmp:
        def __init__(self):
            if use is not NEW_ONLY:
                self.old = iter(old)
            if use is not OLD_ONLY:
                self.new = iter(new)

    c = Cmp()
    if use is OLD_ONLY:
        assert seq(c) == old
    elif use is NEW_ONLY:
        assert seq(c) == new
    elif old == new:
        assert seq(c) == old
    else:
        with pytest.raises(StrangledDifference) as exc:
            seq(c)
        check_strangler_exc(exc, "Cmp.__iter__", f"{old}", f"{new}")
    assert no_strangler_logging()


def seq(numbers):
    return [number for number in numbers]
