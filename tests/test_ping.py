def test_health_check_success(session, base_url):
    response = session.get(f"{base_url}/ping")
    assert response.text == "Created"
    assert response.status_code == 201

def test_health_check_invalid_method(session, base_url):
    response = session.post(f"{base_url}/ping")
    assert response.status_code == 404