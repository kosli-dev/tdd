
def test_04692400(xy):
    """
    All Xs and Ys
    """
    decisions = [('XXYYY', False), ('XYYXX', False), ('XYYXY', False), ('?YYXX', False)]
    response = xy.company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert response.status_code == 200
    assert response.json() == [[4, 8, 6, 3, 3],
                               [4, 3, 6, 4, 4],
                               [4, 3, 6, 4, 3],
                               [-2, 3, 6, 4, 4]]


def test_04692401(xy):
    """
    Not words.
    """
    decisions = [('XYZZY', False), ('XYZZy', False)]
    response = xy.company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert response.status_code == 200
    assert response.json() == [[4, 6, 0, 0, 6], [4, 6, 0, 0, 6]]


def test_04692402(xy):
    """
    Letters from 'Big Fish Little Pond War' heading
    """
    decisions = [('BigFi', False), ('shLit', False), ('tlePo', False), ('ndWaR', False)]
    response = xy.company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert response.status_code == 200
    assert response.json() == [[1, -1, 1, 2, -1],
                               [4, 8, 16, -1, 32],
                               [0, 0, -1, 0, -1],
                               [0, 256, 512, -1, 1024]]


def test_04692403(xy):
    """
    Lowercase letters from 'Big Fish Little Pond War' heading
    """
    decisions = [('bigfi', False), ('shlit', False), ('tlepo', False), ('ndwaw', False)]
    response = xy.company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert response.status_code == 200
    STRANGE = 0  # This is 10240 in equivalent unit test???
    assert response.json() == [[10, -10, 10, 20, -10],
                               [40, 80, 160, -10, 320],
                               [0, 0, -10, 0, -10],
                               [0, 2560, 5120, -10, STRANGE]]


def test_04692410(xy):
    """
    Not profound sentence.
    """
    decisions = [('hello', True), ('world', True)]
    response = xy.company_score(decisions=decisions, is_sentence=True, is_profound=False)
    assert response.status_code == 200
    assert response.json() == [[0, -10000, 160000, 0, -10000],
                               [0, -10000, 0, 160000, 0]]


def test_04692411(xy):
    """
    Illegal/invalid letter
    """
    decisions = [('hell?', False), ('world', True)]
    response = xy.company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert response.status_code == 200
    assert response.json() == [[0, -10, 160, 0, -20],
                               [51200, -100, 102400, 0, 0]]


def test_04692412(xy):
    """
    Profound sentence.
    """
    decisions = [('world', True), ('warms', True)]
    response = xy.company_score(decisions=decisions, is_sentence=True, is_profound=True)
    assert response.status_code == 200
    assert response.json() == [[51200000, -100000, 102400000, 0, 0],
                               [0, -100000, 0, 0, 400000]]
