
def test_c8e1d000(app):
    """
    """
    result = app.company_score()
    assert result.status_code == 200
