from strangler import call_old, call_new
from strangler import OLD_ONLY, OLD_MAIN, NEW_MAIN, NEW_ONLY


def test_760e00():
    """
    call_old() is False only for NEW_ONLY
    """
    assert call_old(OLD_ONLY)
    assert call_old(OLD_MAIN)
    assert call_old(NEW_MAIN)
    assert call_old(NEW_ONLY) is False


def test_760e01():
    """
    call_new() is False only for OLD_ONLY
    """
    assert call_new(OLD_ONLY) is False
    assert call_new(OLD_MAIN)
    assert call_new(NEW_MAIN)
    assert call_new(NEW_ONLY)


def test_760e02():
    """
    Four switches must all be unique.
    """
    unique = set()
    for s in [OLD_ONLY, OLD_MAIN, NEW_MAIN, NEW_ONLY]:
        unique.add(s)
    assert len(unique) == 4
