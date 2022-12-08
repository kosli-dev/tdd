import bs4


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

    soup = bs4.BeautifulSoup(result.text, 'html.parser')
    scores_div = soup.find("div", id='scores')
    score_panels = scores_div.find_all('div', class_='panel')
    score_text = [panel.getText() for panel in score_panels]
    assert score_text == [
        '\n        Squad-A\n        \n        Score==140==[0, -10, 160, 0, -10]\n    ',
        '\n        Squad-B\n        \n        Score==150==[0, -10, 0, 160, 0]\n    ',
        '\n        Squad-C\n        \n        Score==220==[80, -10, 0, 160, -10]\n    ',
    ]

    # TODO: assert redirected to app.scores(sid)


def test_c8e1d002(app):
    """
    The page for scoring an entered squad's decisions will redirect to score.html if the
    request payload is invalid.
    """
    result = app.post_company_score({
        "invalid": "format"
    })
    # TODO: This test needs some work, but it's not clear to me what's expected. In the handler for the post,
    # the input data is validated. If it fails validation, it's still passed to the score.html template, even
    # though the template won't generally be able to use invalid data. Maybe the data I'm using is *too*
    # invalid.
    #
    # So for now we're just asserting on the 500 and leaving refinement for later.

    assert result.status_code == 500