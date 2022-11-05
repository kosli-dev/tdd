
def test_c8e1d000(app):
    """
    The number of squads in a company is controlled
    by the n argument.
    """
    result = app.company_score(n=3)
    assert result.status_code == 200
    result = app.company_score(n=4)
    assert result.status_code == 200
