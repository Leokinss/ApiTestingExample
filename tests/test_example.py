def test_health_check(session, base_url):
    response = session.get(f"{base_url}/health")
    assert response.status_code == 200
