
def test_04692400(xy):
    """
    ........
    """
    decisions = [('XYZZY', False), ('XYZZy', False)]
    response = xy.company_score(decisions=decisions, is_sentence=False, is_profound= False)
    assert response.status_code == 200
    assert response.json() == [[8, 5, 0, 0, 5], [0, -1, 16, 0, -1]]


def test_04692401(xy):
    """
    ........
    """
    decisions = [('hello', True), ('world', True)]
    response = xy.company_score(decisions=decisions, is_sentence=True, is_profound= False)
    assert response.status_code == 200
    assert response.json() == [[4, 5, 0, 0, 5], [4, 5, 0, 0, 5]]


def test_04692402(xy):
    """
    ........
    """
    assert 2 == 2
