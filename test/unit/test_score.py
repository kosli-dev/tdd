from model import company_score

EXPECTED = {
    'invalid_entry': 76,
    'all_Xs_and_Ys': 82,
    'letters_from_heading': 1850,
    'only_lowercase_letters_from_heading': 18500,
    'only_lowercase_consonants_near_end_of_heading': 40960,
    'sentence_of_lowercase_5_letter_words': 16840000,
    'better_sentence_of_lowercase_5_letter_words': 17310000,
    'profound_sentence_of_lowercase_5_letter_words': 207000000,
}


def test_5386b900():
    """Level 1: Invalid entries are written as ?"""
    decisions = go('XXYYY'), go('XYYXX'), go('XYYXY'), go('?YYXX')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[4, 8, 5, 3, 3],
                      [4, 3, 5, 4, 4],
                      [4, 3, 5, 4, 3],
                      [-2, 3, 5, 4, 4]]
    assert sum(flatten(scores)) == EXPECTED['invalid_entry']


def test_5386b901():
    """Level 2: All Xs and Ys"""
    decisions = go('XXYYY'), go('XYYXX'), go('XYYXY'), go('XYYXX')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[4, 8, 5, 3, 3],
                      [4, 3, 5, 4, 4],
                      [4, 3, 5, 4, 3],
                      [4, 3, 5, 4, 4]]
    assert sum(flatten(scores)) == EXPECTED['all_Xs_and_Ys']


def test_5386b902():
    """Level 3: Letters from 'Big Fish Little Pond War' heading"""
    decisions = go('BigFi'), go('shLit'), go('tlePo'), go('ndWaR')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[1, -1, 1, 2, -1],
                      [4, 8, 16, -1, 32],
                      [0, 0, -1, 0, -1],
                      [0, 256, 512, -1, 1024]]
    assert sum(flatten(scores)) == EXPECTED['letters_from_heading']


def test_5386b903():
    """Level 4: Only lowercase letters from 'Big Fish Little Pond War' heading"""
    decisions = go('bigfi'), go('shlit'), go('tlepo'), go('ndwar')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[10, -10, 10, 20, -10],
                      [40, 80, 160, -10, 320],
                      [0, 0, -10, 0, -10],
                      [0, 2560, 5120, -10, 10240]]
    assert sum(flatten(scores)) == EXPECTED['only_lowercase_letters_from_heading']


def test_5386b904():
    """Level 5: Only lowercase consonants near end of heading"""
    decisions = go('rrrrr'), go('rrrrr'), go('rrrrr'), go('rrrrr')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[0, 10240, 0, 0, 0],
                      [0, 0, 10240, 0, 0],
                      [0, 0, 0, 10240, 0],
                      [0, 0, 0, 0, 10240]]
    assert sum(flatten(scores)) == EXPECTED['only_lowercase_consonants_near_end_of_heading']


def test_5386b905():
    """Unconnected lowercase 5 letter words (scores can get worse)"""
    decisions = word('dwarf'), word('rules'), word('knife'), go('wwwww')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[0, 0, -100, 0, 200],
                      [0, -100, 1600, -100, 400],
                      [0, 0, -100, 200, -100],
                      [0, 0, 0, 5120, 0]]
    assert sum(flatten(scores)) == 7020


def test_5386b906():
    """Level 6: sentence of lowercase 5 letter words"""
    decisions = word('wrong'), word('words'), word('score'), word('small')
    scores = company_score(decisions=decisions, is_sentence=True, is_profound=False)
    assert scores == [[5120000, 10240000, -10000, 1280000, 10000],
                      [0, -10000, 0, 0, 40000],
                      [0, 0, -10000, 0, -10000],
                      [40000, 0, -10000, 160000, 0]]
    assert sum(flatten(scores)) == EXPECTED['sentence_of_lowercase_5_letter_words']


def test_5386b907():
    """Level 7: better sentence of lowercase 5 letter words"""
    decisions = word('wrote'), word('wrong'), word('wrote'), word('wrath')
    scores = company_score(decisions=decisions, is_sentence=True, is_profound=False)
    assert scores == [[5120000, 10240000, -10000, 320000, -10000],
                      [0, 0, -10000, 1280000, 10000],
                      [0, 0, -10000, 0, -10000],
                      [0, 0,-10000, 320000, 80000]]
    assert sum(flatten(scores)) == EXPECTED['better_sentence_of_lowercase_5_letter_words']


def X_test_5386b908():
    """Level 8: profound_sentence_of_lowercase_5_letter_words"""
    decisions = word('waits'), word('while'), word('world'), word('warms')
    scores = company_score(decisions=decisions, is_sentence=True, is_profound=True)
    assert scores == [[51200000, -100000, -100000, 0, 0],
                      [0, 800000, -100000, 1600000, -100000],
                      [51200000, -100000, 102400000, 0, 0],
                      [0, -100000, 0, 0, 400000]]
    expected = EXPECTED['better_sentence_of_lowercase_5_letter_words']
    assert sum(flatten(scores)) == expected


def test_5386b920():
    """ Scores increase as fortune cookies levels are unlocked"""
    s1 = EXPECTED['invalid_entry']
    s2 = EXPECTED['all_Xs_and_Ys']
    s3 = EXPECTED['letters_from_heading']
    s4 = EXPECTED['only_lowercase_letters_from_heading']
    s5 = EXPECTED['only_lowercase_consonants_near_end_of_heading']
    #             'unconnected_lowercase_5_letter_words'
    s6 = EXPECTED['sentence_of_lowercase_5_letter_words']
    s7 = EXPECTED['better_sentence_of_lowercase_5_letter_words']
    s8 = EXPECTED['profound_sentence_of_lowercase_5_letter_words']
    assert is_sorted([s1, s2, s3, s4, s5, s6, s7, s8]), 'Level scores must increase!'


def go(s):
    return [s, False]


def word(s):
    return [s, True]


def is_sorted(s):
    return all(s[i] <= s[i+1] for i in range(len(s) - 1))


def flatten(arg):
    return [item for sublist in arg for item in sublist]
