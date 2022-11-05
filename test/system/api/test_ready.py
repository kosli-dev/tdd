
def test_bf0d8000(api):
    """
    api/health/ready is 200
    """
    response = api.health_ready()
    assert response.status_code == 200
