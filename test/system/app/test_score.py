
def test_c8e1d000(app):
    """
    There is a page for entering squads decisions.
    The number of squads in a company is controlled
    by the n argument.
    """
    result = app.get_company_score(n=3)
    assert result.status_code == 200
    result = app.get_company_score(n=4)
    assert result.status_code == 200


def test_c8e1d001(app):
    """
    There is a page for scoring an entered squads decisions.
    """
    result = app.post_company_score(
        squads=[
            {"letters": "hello", "is_word": True},
            {"letters": "world", "is_word": True}
        ],
        is_sentence=False,
        is_profound=False
    )
    assert result.status_code == 200
    # TODO: assert redirected to app.scores(sid)
