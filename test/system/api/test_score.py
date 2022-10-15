
def test_04692400(xy):
    """
    ........
    """
    response = xy.score()
    assert response.status_code == 200
    assert response.json() == {"A": 23, "B": 1245, "C": 78}


def test_04692401(xy):
    """
    ........
    """
    assert 2 == 2
