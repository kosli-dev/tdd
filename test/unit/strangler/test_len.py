import pytest
from strangler import *
from .helpers import *
# from helpers.unit.lib.scoped_env_var import ScopedEnvVar


def test_18011400(t):
    """OLD_ONLY"""
    @strangled_method('__len__', use=OLD_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.old = Len(lambda: 8742)
            self.new = None
    d = Diff()

    assert len(d) == 8742
    assert no_cc_logging()


def test_18011401(t):
    """NEW_TEST On Same"""
    @strangled_method('__len__', use=NEW_TEST, kind="query")
    class Same:
        def __init__(self):
            self.old = Len(lambda: 5)
            self.new = Len(lambda: 5)
    s = Same()

    assert len(s) == 5
    assert no_cc_logging()


def test_18011402(t):
    """NEW_TEST On Different"""
    @strangled_method('__len__', use=NEW_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.old = Len(lambda: 69)
            self.new = Len(lambda: 56)
    d = Diff()

    with pytest.raises(StrangledDifference) as exc:
        len(d)
    check_exc_log(exc.value, 'Diff', '__len__', '69', '56')
    assert no_cc_logging()


def test_18011403(t):
    """NEW_TEST Off Different"""
    @strangled_method('__len__', use=NEW_TEST, kind="query")
    class Diff:
        def __init__(self):
            self.old = Len(lambda: 23)
            self.new = Len(lambda: raiser())
    d = Diff()

    with ScopedEnvVar('TEST_MODE', 'not-unit'):
        assert len(d) == 23
    assert no_cc_logging()


def test_18011404(t):
    """OLD_MAIN Same"""
    @strangled_method('__len__', use=OLD_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.old = Len(lambda: 4228)
            self.new = Len(lambda: 4228)
    s = Same()

    assert len(s) == 4228
    assert no_cc_logging()


def test_18011405(t):
    """OLD_MAIN Different"""
    @strangled_method('__len__', use=OLD_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.old = Len(lambda: 517)
            self.new = Len(lambda: 518)
    d = Diff()

    assert len(d) == 517
    check_cm_log('517', '518')


def test_18011407(t):
    """NEW_MAIN Different"""
    @strangled_method('__len__', use=NEW_MAIN, kind="query")
    class Diff:
        def __init__(self):
            self.old = Len(lambda: raiser())
            self.new = Len(lambda: 45)
    d = Diff()

    assert len(d) == 45
    check_cm_log('not-set', '45')


def test_18011408(t):
    """NEW_MAIN Same"""
    @strangled_method('__len__', use=NEW_MAIN, kind="query")
    class Same:
        def __init__(self):
            self.old = Len(lambda: 7)
            self.new = Len(lambda: 7)
    s = Same()

    assert len(s) == 7
    assert no_cc_logging()


def test_18011409(t):
    """NEW_ONLY"""
    @strangled_method('__len__', use=NEW_ONLY, kind="query")
    class Diff:
        def __init__(self):
            self.old = None
            self.new = Len(lambda: 1212)
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
