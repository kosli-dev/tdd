import pytest

MARKED_PARAMS = []


def test_d4f4f0(t):
    """
    Using a t fixture means you can write the
    test description in the docstring, like this,
    in free form, of any length you like, over
    as many lines as you like.
    """
    assert t.id == "d4f4f0"


@pytest.mark.parametrize('arg', [1, 2, 3, 4])
def test_d4f4f1(t, arg):
    """
    When a test has a t fixture and has parameterized data
    then t will be passed multiple times, so provide t.n which
    is unique each time the test is run in case the tests need
    to use this to ensure they are truly isolated from each other
    """
    MARKED_PARAMS.append(t.n)
    if len(MARKED_PARAMS) == 4:
        assert sorted(MARKED_PARAMS) == [1, 2, 3, 4]  # parameters are in random order
