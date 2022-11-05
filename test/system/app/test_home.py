
def test_c8e1d000(app):
    """
    """
    result = app.home()
    assert result.status_code == 200
