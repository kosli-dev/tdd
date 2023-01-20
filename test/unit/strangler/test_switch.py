from strangler import old_is_on, new_is_on
from strangler import OLD_ONLY, NEW_TEST, OLD_MAIN, NEW_MAIN, NEW_ONLY


def test_760e00():
    """
    old_is_on() is False only for NEW_ONLY
    """
    eg = Eg(True, None)
    assert old_is_on(eg, OLD_ONLY)
    assert old_is_on(eg, NEW_TEST)
    assert old_is_on(eg, OLD_MAIN)
    assert old_is_on(eg, NEW_MAIN)
    assert old_is_on(eg, NEW_ONLY) is False


def test_760e01():
    """
    new_is_on() is False only for OLD_ONLY
    """
    eg = Eg(None, True)
    assert new_is_on(eg, OLD_ONLY) is False
    assert new_is_on(eg, NEW_TEST)
    assert new_is_on(eg, OLD_MAIN)
    assert new_is_on(eg, NEW_MAIN)
    assert new_is_on(eg, NEW_ONLY)


def test_760e02():
    """
    Five switches must all be unique.
    """
    unique = set()
    for s in [OLD_ONLY, NEW_TEST, OLD_MAIN, NEW_MAIN, NEW_ONLY]:
        unique.add(s)
    assert len(unique) == 5


class Eg:
    def __init__(self, o, n):
        self.old = o
        self.new = n
