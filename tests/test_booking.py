import pytest

# Create a factory fixture to generate booking data for tests because it is a common step.
@pytest.fixture
def booking_factory(session, base_url):
    def _create(overrides=None):
        booking_data = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-10"
            },
            "additionalneeds": "Breakfast"
        }

        headers = {"Content-Type": "application/json"}
        if overrides:
            booking_data.update(overrides)

        response = session.post(f"{base_url}/booking", headers=headers, json=booking_data)
        assert response.status_code == 200

        return response.json(), booking_data

    return _create

def test_create_booking_success(session, base_url, booking_factory):

    response_data, expected_booking_data = booking_factory()
    assert response_data["booking"] == expected_booking_data
    assert "bookingid" in response_data
    assert isinstance(response_data["bookingid"], int)

def test_create_and_get_booking_id(session, base_url, booking_factory):
    response_data, expected_booking_data = booking_factory()
    booking_id = response_data["bookingid"]

    get_response = session.get(f"{base_url}/booking/{booking_id}")
    assert get_response.status_code == 200
    assert get_response.json() == expected_booking_data

def test_get_all_booking_ids(session, base_url):
    response = session.get(f"{base_url}/booking")
    assert response.status_code == 200
    assert isinstance(response.json(), list)