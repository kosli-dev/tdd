
def test_04692400(xy):
    """
    ........
    """
    decisions = [('XYZZY', False), ('hello', True)]
    response = xy.company_score(decisions=decisions, is_sentence=False, is_profound= False)
    assert response.status_code == 200
    assert response.json() == [[8, 5, 0, 0, 5], [0, -1, 16, 0, -1]]


def test_04692401(xy):
    """
    ........
    """
    assert 2 == 2
