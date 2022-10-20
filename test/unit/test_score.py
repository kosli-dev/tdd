from model import company_score


def test_86b900():
    """
    Level 1:
    Invalid entries are written as ?
    """
    decisions = go('XXYYY'), go('XYYXX'), go('XYYXY'), go('?YYXX')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[4, 8, 5, 3, 3],
                      [4, 3, 5, 4, 4],
                      [4, 3, 5, 4, 3],
                      [-2, 3, 5, 4, 4]]
    assert sum(flatten(scores)) == EXPECTED['invalid_entry']


def test_86b901():
    """
    Level 2:
    All Xs and Ys
    """
    decisions = go('XXYYY'), go('XYYXX'), go('XYYXY'), go('XYYXX')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[4, 8, 5, 3, 3],
                      [4, 3, 5, 4, 4],
                      [4, 3, 5, 4, 3],
                      [4, 3, 5, 4, 4]]
    assert sum(flatten(scores)) == EXPECTED['all_Xs_and_Ys']


def test_86b902():
    """
    Level 3:
    Letters from 'Big Fish Little Pond War' heading
    """
    decisions = go('BigFi'), go('shLit'), go('tlePo'), go('ndWaR')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[1, -1, 1, 2, -1],
                      [4, 8, 16, -1, 32],
                      [0, 0, -1, 0, -1],
                      [0, 256, 512, -1, 1024]]
    assert sum(flatten(scores)) == EXPECTED['letters_from_heading']


def test_86b903():
    """
    Level 4:
    Only lowercase letters from 'Big Fish Little Pond War' heading
    """
    decisions = go('bigfi'), go('shlit'), go('tlepo'), go('ndwar')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[10, -10, 10, 20, -10],
                      [40, 80, 160, -10, 320],
                      [0, 0, -10, 0, -10],
                      [0, 2560, 5120, -10, 10240]]
    assert sum(flatten(scores)) == EXPECTED['only_lowercase_letters_from_heading']


def test_86b904():
    """
    Level 5:
    Only lowercase consonants near end of heading
    """
    decisions = go('rrrrr'), go('rrrrr'), go('rrrrr'), go('rrrrr')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[0, 10240, 0, 0, 0],
                      [0, 0, 10240, 0, 0],
                      [0, 0, 0, 10240, 0],
                      [0, 0, 0, 0, 10240]]
    assert sum(flatten(scores)) == EXPECTED['only_lowercase_consonants_near_end_of_heading']


def test_86b905():
    """
    Unconnected lowercase words (scores can get worse)
    """
    decisions = word('dwarf'), word('rules'), word('knife'), go('wwwww')
    scores = company_score(decisions=decisions, is_sentence=False, is_profound=False)
    assert scores == [[0, 0, -100, 0, 200],
                      [0, -100, 1600, -100, 400],
                      [0, 0, -100, 200, -100],
                      [0, 0, 0, 5120, 0]]
    assert sum(flatten(scores)) == 7020


def test_86b906():
    """
    Level 6:
    Sentence of lowercase words
    """
    decisions = word('wrong'), word('words'), word('score'), word('small')
    scores = company_score(decisions=decisions, is_sentence=True, is_profound=False)
    assert scores == [[5120000, 10240000, -10000, 1280000, 10000],
                      [0, -10000, 0, 0, 40000],
                      [0, 0, -10000, 0, -10000],
                      [40000, 0, -10000, 160000, 0]]
    assert sum(flatten(scores)) == EXPECTED['sentence_of_lowercase_words']


def test_86b907():
    """
    Level 7:
    Better sentence of lowercase words
    """
    decisions = word('wrote'), word('wrong'), word('wrote'), word('wrath')
    scores = company_score(decisions=decisions, is_sentence=True, is_profound=False)
    assert scores == [[5120000, 10240000, -10000, 320000, -10000],
                      [0, 0, -10000, 1280000, 10000],
                      [0, 0, -10000, 0, -10000],
                      [0, 0,-10000, 320000, 80000]]
    assert sum(flatten(scores)) == EXPECTED['better_sentence_of_lowercase_words']


def test_86b908():
    """
    Level 8:
    Profound sentence of lowercase words
    """
    decisions = word('waits'), word('while'), word('world'), word('warms')
    scores = company_score(decisions=decisions, is_sentence=True, is_profound=True)
    assert scores == [[51200000, -100000, -100000, 0, 0],
                      [0, 800000, -100000, 1600000, -100000],
                      [51200000, -100000, 102400000, 0, 0],
                      [0, -100000, 0, 0, 400000]]
    assert sum(flatten(scores)) == EXPECTED['profound_sentence_of_lowercase_words']


def test_86b909():
    """Example with 3 squads"""
    decisions = word('waits'), word('while'), word('world')
    scores = company_score(decisions=decisions, is_sentence=True, is_profound=True)
    assert scores == [[51200000, -100000, -100000, 0, 0],
                      [0, 800000, -100000, 1600000, -100000],
                      [51200000, -100000, 102400000, 0, 0]]


"""
XY Scoring Table is as follows:
                      X Y
All squads play Y     0 5
One squad plays Y     8 3
Two+ squads play Y    4 3

The important property of this table is that for
a company of 3 or more squads choosing all Y's gives
the biggest company score.

3 squads
   0X,3Y ==   0 + 3*5 == 0+15 == 15 <===
   1X,2Y == 1*8 + 2*3 == 8+6  == 14
   2X,1Y == 2*4 + 1*3 == 8+3  == 11
   3X,0Y == 3*4 +   0 == 12+0 == 12
4 squads
   0X,4Y ==   0 + 4*5 == 0+20 == 20 <===
   1X,3Y == 1*8 + 3*3 == 8+9  == 17
   2X,2Y == 2*4 + 2*3 == 8+6  == 14
   3X,1Y == 1*4 + 3*3 == 4+9  == 13
   4X,0Y == 4*4 +   0 == 16+0 == 16
5 squads
   0X,5Y ==   0 + 5*5 == 0+25 == 25 <===
   1X,4Y == 1*8 + 4*3 == 8+12 == 20
   2X,3Y == 2*4 + 3*3 == 8+9  == 17
   3X,2Y == 3*4 + 2*3 == 12+6 == 18
   4X,1Y == 4*4 + 1*3 == 16+3 == 19
   5X,0Y == 5*4 +   0 == 20+0 == 20
6 squads
   0X,6Y ==   0 + 6*5 == 0+30 == 30 <===
   1X,5Y == 1*8 + 5*3 == 8+15 == 23
   2X,4Y == 2*4 + 4*3 == 8+12 == 20
   3X,3Y == 3*4 + 3*3 == 12+9 == 21
   4X,2Y == 4*4 + 2*3 == 16+6 == 22
   5X,1Y == 5*4 + 1*3 == 20+3 == 23
   6X,0Y == 6*4 +   0 == 24+0 == 24
"""


def test_86b920():
    """ Scores increase as fortune cookies levels are unlocked"""
    s1 = EXPECTED['invalid_entry']
    s2 = EXPECTED['all_Xs_and_Ys']
    s3 = EXPECTED['letters_from_heading']
    s4 = EXPECTED['only_lowercase_letters_from_heading']
    s5 = EXPECTED['only_lowercase_consonants_near_end_of_heading']
    #             'unconnected_lowercase_words'
    s6 = EXPECTED['sentence_of_lowercase_words']
    s7 = EXPECTED['better_sentence_of_lowercase_words']
    s8 = EXPECTED['profound_sentence_of_lowercase_words']
    assert is_sorted([s1, s2, s3, s4, s5, s6, s7, s8]), 'Level scores must increase!'


EXPECTED = {
    'invalid_entry': 76,
    'all_Xs_and_Ys': 82,
    'letters_from_heading': 1850,
    'only_lowercase_letters_from_heading': 18500,
    'only_lowercase_consonants_near_end_of_heading': 40960,
    'sentence_of_lowercase_words': 16840000,
    'better_sentence_of_lowercase_words': 17310000,
    'profound_sentence_of_lowercase_words': 207000000,
}


def go(s):
    return [s, False]


def word(s):
    return [s, True]


def is_sorted(s):
    return all(s[i] <= s[i+1]
               for i in range(len(s) - 1))


def flatten(arg):
    return [item
            for sublist in arg
            for item in sublist]
