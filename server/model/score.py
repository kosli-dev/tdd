

def company_score(*decisions, **kwargs):
    is_sentence = kwargs['is_sentence']
    is_profound = kwargs['is_profound']
    words, are_words = transpose(decisions)
    assert well_formed(words)
    words = [list(word) for word in words]
    multipliers = squad_multipliers(words, are_words, is_sentence, is_profound)
    return [score * multiplier
            for score, multiplier
            in zip(squad_scores(*words), multipliers)]


def squad_scores(*company_decisions):
    scores, n = [], 0
    company_decisions = marked(company_decisions)
    for squad_decisions in company_decisions:
        score, n = squad_score(n, squad_decisions, company_decisions)
        scores.append(score)

    return scores


def squad_score(n, squad_decisions, company_decisions):
    scores = []
    for i in range(0, 5):
        score, n = letter_score(n, squad_decisions[i], ith(company_decisions,i))
        scores.append(score)
    return [scores, n]


def letter_score(n, squad_decision, company_decisions):
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
    if is_invalid_or_illegal(squad_decision):
        score, n = -2, 0
    elif is_vowel(squad_decision):
        score = -1
    elif is_unscoring_consonant(squad_decision):
        score = 0
    elif squad_decision == 'X':
        score = xy_score(0, 8, 4, company_decisions)
    elif squad_decision == 'Y':
        score = xy_score(5, 3, 3, company_decisions)
    else:
        assert squad_decision != '0'  # FIX ME
        score = BIG_FISH_TABLE[n][squad_decision]
        n = (n + 1) % 6

    return [score, n]


INVALID_OR_ILLEGAL = 'invalid_or_illegal'
UNSCORING_CONSONANT = 'unscoring_consonant'

MARKERS = {
  # Jerry's version uses X* for illegal or illegible decisions
  # and Y* for unscoring consonants. I have changed these to
  # '?' and '0' respectively as using single chars simplifies
  # the program, specifically the ability to write
  #    word.chars
  # to get the 5 decision-letters from a 5 character word.
  INVALID_OR_ILLEGAL:  '?',
  UNSCORING_CONSONANT: '0'
}


def is_invalid_or_illegal(decision):
    return decision == MARKERS[INVALID_OR_ILLEGAL]


def is_unscoring_consonant(decision):
    return decision == MARKERS[UNSCORING_CONSONANT]


def is_scoring_consonant(decision):
    return decision.upper() in 'XYBGFSHLTPNDWR'


def is_vowel(decision):
    # [*] Jerry's version scores a vowel as zero.
    # I decided to try a vowel scoring a small negative number.
    # This creates a nice tension since you need vowels to create
    # words. Viz, to get the best score for 5 decisions you need
    # to choose at least one decision that scores badly.
    # Do you want to optimize the parts or the whole?
    return decision.upper() in 'AEIOU'


def xy_score(zero, one, two_or_more, decisions):
    xs = count_X(decisions)
    if xs == 0:
        return zero
    elif xs == 1:
        return one
    else:
        return two_or_more


def count_X(decisions):
    return sum(1 for d in decisions if d == 'X')


def big_fish_values(b, g, f, s, h, l, t, p, n, d, w, r):
    return {
        'B': b, 'G': g, 'F': f, 'S': s, 'H': h,
        'L': l, 'T': t, 'P': p, 'N': n, 'D': d,
        'W': w, 'R': r
    }


BIG_FISH_TABLE = {
    #                  B  G  F  S  H   L   T   P    N    D    W     R
    0: big_fish_values(1, 1, 2, 4, 0,  0, 32,  0,   0,   0, 512,    0),
    1: big_fish_values(1, 1, 2, 4, 8, 16,  0, 64,   0,   0,   0, 1024),
    2: big_fish_values(1, 1, 2, 0, 8,  0, 32,  0, 128,   0,   0,    0),
    3: big_fish_values(1, 1, 2, 4, 0, 16,  0,  0,   0,   0,   0,    0),
    4: big_fish_values(1, 1, 2, 4, 8,  0, 32, 64,   0,   0,   0,    0),
    5: big_fish_values(1, 1, 0, 0, 8, 16,  0,  0, 128, 256,   0,    0),
}


def marked(company_decisions):
    # company_decisions.map do |squad_decisions|
    #   squad_decisions.map do |decision|
    #     if invalid_or_illegal?(decision)
    #       marker_for(:invalid_or_illegal)
    #     elsif vowel?(decision) || scoring_consonant?(decision)
    #       decision.upcase
    #     else
    #       marker_for(:unscoring_consonant)
    #     end
    #   end
    # end
    result = []
    for company_decision in company_decisions:
        part = []
        for letter in company_decision:
            part.append(squad_decision(letter))
        result.append(part)
    return result


def squad_decision(letter):
    if is_invalid_or_illegal(letter):
        return MARKERS[INVALID_OR_ILLEGAL]
    elif is_vowel(letter) or is_scoring_consonant(letter):
        return letter.upper()
    else:
        return MARKERS[UNSCORING_CONSONANT]


def well_formed(goes):
    def all_strings():
        return all(isinstance(go, str) for go in goes)

    def all_len_5():
        return all(len(go) == 5 for go in goes)

    return all_strings() and all_len_5()


def squad_multipliers(letters, are_words, is_sentence, is_profound):
    return [squad_multiplier(all_lower(letters), is_word, is_sentence, is_profound)
            for is_word in are_words]


def squad_multiplier(are_lower, is_word, is_sentence, is_profound):
    multiplier = 1
    if are_lower:
        multiplier = 10
        if is_word:
            multiplier = 100
            if is_sentence:
                multiplier = 10000
                if is_profound:
                    multiplier = 100000
    return multiplier


def ith(arrays, i):
    return [array[i] for array in arrays]


def all_lower(letters):
    return all(letter == letter.lower() for letter in flatten(letters))


def transpose(m):
    return [*zip(*m)]


def flatten(arg):
    return [item for sublist in arg for item in sublist]
