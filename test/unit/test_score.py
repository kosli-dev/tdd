from model import company_score


def test_invalid_entry():
    a, b, c, d = go('XXYYY'), go('XYYXX'), go('XYYXY'), go('?YYXX')
    scores = company_score(a, b, c, d, is_sentence=False, is_profound=False)
    assert scores == [[4, 8, 5, 3, 3], [4, 3, 5, 4, 4], [4, 3, 5, 4, 3], [-2, 3, 5, 4, 4]]
    assert_sums([23, 20, 19, 14], scores)
    assert sum(flatten(scores)) == 76
    return 76


def test_all_Xs_and_Ys():
    a, b, c, d = go('XXYYY'), go('XYYXX'), go('XYYXY'), go('XYYXX')
    scores = company_score(a, b, c, d, is_sentence=False, is_profound=False)
    assert scores == [[4, 8, 5, 3, 3], [4, 3, 5, 4, 4], [4, 3, 5, 4, 3], [4, 3, 5, 4, 4]]
    assert_sums([23, 20, 19, 20], scores)
    assert sum(flatten(scores)) == 82
    return 82


def test_letters_from_heading():
    a, b, c, d = go('BigFi'), go('shLit'), go('tlePo'), go('ndWaR')
    scores = company_score(a, b, c, d, is_sentence=False, is_profound=False)
    assert scores == [[1, -1, 1, 2, -1], [4, 8, 16, -1, 32], [0, 0, -1, 0, -1], [0, 256, 512, -1, 1024]]
    assert_sums([2, 59, -2, 1791], scores)
    assert sum(flatten(scores)) == 1850
    return 1850


def test_scores_increase_as_fortune_cookies_are_unlocked():
    s0 = test_invalid_entry()
    s1 = test_all_Xs_and_Ys()
    s2 = test_letters_from_heading()
    assert is_sorted([s0, s1, s2]), 'not sorted!'


def assert_sums(expected, scores):
    for i in range(0, len(scores)):
        assert expected[i] == sum(scores[i])


def go(s):
    return [s, False]


def is_sorted(s):
    return all(s[i] <= s[i+1] for i in range(len(s) - 1))


def flatten(arg):
    return [item for sublist in arg for item in sublist]
