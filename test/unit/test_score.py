from model import company_score

EXPECTED = {
    'invalid_entry': 76,
    'all_Xs_and_Ys': 82,
    'letters_from_heading': 1850,
    'only_lowercase_letters_from_heading': 18500
}


def test_invalid_entry():
    decisions = go('XXYYY'), go('XYYXX'), go('XYYXY'), go('?YYXX')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[4, 8, 5, 3, 3],
                      [4, 3, 5, 4, 4],
                      [4, 3, 5, 4, 3],
                      [-2, 3, 5, 4, 4]]
    assert sum(flatten(scores)) == EXPECTED['invalid_entry']


def test_all_Xs_and_Ys():
    decisions = go('XXYYY'), go('XYYXX'), go('XYYXY'), go('XYYXX')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[4, 8, 5, 3, 3],
                      [4, 3, 5, 4, 4],
                      [4, 3, 5, 4, 3],
                      [4, 3, 5, 4, 4]]
    assert sum(flatten(scores)) == EXPECTED['all_Xs_and_Ys']


def test_letters_from_heading():
    decisions = go('BigFi'), go('shLit'), go('tlePo'), go('ndWaR')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[1, -1, 1, 2, -1],
                      [4, 8, 16, -1, 32],
                      [0, 0, -1, 0, -1],
                      [0, 256, 512, -1, 1024]]
    assert sum(flatten(scores)) == EXPECTED['letters_from_heading']


def X_test_only_lowercase_letters_from_heading():
    decisions = go('bigfi'), go('shlit'), go('tlepo'), go('ndwar')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[10, -10, 10, 20, -10],
                      [40, 80, 160, -10, 320],
                      [0, 0, -10, 0, -10],
                      [0, 2560, 5120, -10, 10240]]
    assert sum(flatten(scores)) == EXPECTED['only_lowercase_letters_from_heading']


def test_scores_increase_as_fortune_cookies_are_unlocked():
    s0 = EXPECTED['invalid_entry']
    s1 = EXPECTED['all_Xs_and_Ys']
    s2 = EXPECTED['letters_from_heading']
    s3 = EXPECTED['only_lowercase_letters_from_heading']
    assert is_sorted([s0, s1, s2, s3]), 'not sorted!'


def go(s):
    return [s, False]


def is_sorted(s):
    return all(s[i] <= s[i+1] for i in range(len(s) - 1))


def flatten(arg):
    return [item for sublist in arg for item in sublist]
