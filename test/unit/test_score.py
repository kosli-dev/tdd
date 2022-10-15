from model import score


def test_a2189656(t):
    """
    Score all Xs and Ys
    """
    assert t.id == "a2189656"
    points = score()
    assert points == {"A": 23, "B": 1245, "C": 78}


# def test_all_Xs_and_Ys
#   a,b,c,d = blah('XXYYY'), blah('XYYXX'), blah('XYYXY'), blah('XYYXX')
#   scores = company_score(sentence=false, profound=false, a,b,c,d)
#   assert_equal([[4,8,5,3,3],[4,3,5,4,4],[4,3,5,4,3],[4,3,5,4,4]], scores)
#   assert_sums([23, 20, 19, 20], scores)
#   assert_equal(total=82, sum(scores))
#   total
# end
