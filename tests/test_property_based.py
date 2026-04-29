import schemathesis

# Automatically generate property-based tests using schemathesis library
# The schema fixture is defined in conftest.py and will be used to generate test cases based on the swagger.json specification.

schema = schemathesis.pytest.from_fixture("schemathesis_schema")

# Covers: GET /ping, POST /auth, GET /booking, POST /booking, GET /booking/{id}
@schema.exclude(method=["PUT", "PATCH", "DELETE"]).parametrize()
def test_public_endpoints(case):
    case.call_and_validate(headers={"Content-Type": "application/json"})

# Covers: PUT /booking/{id}, PATCH /booking/{id}, DELETE /booking/{id}
@schema.include(method=["PUT", "PATCH", "DELETE"]).parametrize()
def test_authenticated_endpoints(case, auth_token):
    headers = {"Cookie": f"token={auth_token}", "Content-Type": "application/json"}
    if case.method.upper() in ["PUT", "PATCH"]:
        headers["Accept"] = "application/json"
    case.call_and_validate(headers=headers)
