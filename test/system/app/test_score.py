
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
    # On server, POST had raw data like this...
    # "squads-0-letters": "hello",
    # "squads-1-letters": "world",
    # "squads-2-letters": "hello",
    # "squads-2_is_word": True,
    # "is_sentence": False,
    # "is_profound": False,

    result = app.post_company_score({
        "squads-0-letters": "hello",
        "squads-1-letters": "world",
        "squads-2-letters": "hello",
        "squads-2_is_word": True,
        "is_sentence": False,
        "is_profound": False,
    })
    assert result.status_code == 200

    # TODO: assert redirected to app.scores(sid)


def test_c8e1d002(app):
    """
    The page for scoring an entered squad's decisions will redirect to score.html if the
    request payload is invalid.
    """
    result = app.post_company_score({
        "invalid": "format"
    })
    assert result.status_code == 500