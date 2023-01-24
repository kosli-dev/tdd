
def company_score(**kwargs):
    decisions = kwargs['decisions']
    is_sentence = kwargs['is_sentence']
    is_profound = kwargs['is_profound']
    words, are_words = transpose(decisions)
    assert well_formed(words)
    words = [list(word) for word in words]
    multipliers = squad_multipliers(words, are_words, is_sentence, is_profound)
    return [[score * multiplier for score in scores]
            for scores, multiplier
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
        score, n = letter_score(n, squad_decisions[i], ith(company_decisions, i))
        scores.append(score)
    return scores, n


def letter_score(n, squad_decision, company_decisions):
    if is_invalid_or_illegal(squad_decision):
        score, n = -2, 0
    elif is_vowel(squad_decision):
        score = -1
    elif is_unscoring_consonant(squad_decision):
        score = 0
    elif squad_decision == 'X':
        score = xy_score(0, 8, 4, company_decisions)
    elif squad_decision == 'Y':
        score = xy_score(6, 3, 3, company_decisions)
    else:
        score = BIG_FISH_TABLE[n][squad_decision]
        n = (n + 1) % 6

    return score, n


INVALID_OR_ILLEGAL = 'invalid_or_illegal'
UNSCORING_CONSONANT = 'unscoring_consonant'

MARKERS = {
  # Jerry's version uses X* for illegal or illegible decisions
  # and Y* for unscoring consonants. I have changed these to
  # '?' and '0' respectively as using single chars simplifies
  # the program, specifically the ability to get 5 decision-letters
  # from a 5 character word.
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
    return [[squad_decision(letter) for letter in company_decision]
            for company_decision in company_decisions]


def squad_decision(letter):
    if is_invalid_or_illegal(letter):
        return MARKERS[INVALID_OR_ILLEGAL]
    elif is_vowel(letter) or is_scoring_consonant(letter):
        return letter.upper()
    else:
        return MARKERS[UNSCORING_CONSONANT]


def well_formed(goes):
    all_strings = all(isinstance(go, str) for go in goes)
    all_len_5 = all(len(go) == 5 for go in goes)
    return all_strings and all_len_5


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
