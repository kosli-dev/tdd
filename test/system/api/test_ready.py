
def test_bf0d8000(xy):
    """
    api/health/ready is 200
    """
    response = xy.health_ready()
    assert response.status_code == 200
