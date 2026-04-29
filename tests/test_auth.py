def test_create_token_success(session, base_url, credentials):
    response = session.post(f"{base_url}/auth", json=credentials)
    token = response.json().get("token")
    assert response.status_code == 200
    assert token is not None
    assert isinstance(token, str)

def test_create_token_invalid_credentials(session, base_url):
    invalid_credentials = {"username": "invalid", "password": "wrong"}
    response = session.post(f"{base_url}/auth", json=invalid_credentials)
    reason = response.json().get("reason")
    assert response.status_code == 200
    assert reason == "Bad credentials"