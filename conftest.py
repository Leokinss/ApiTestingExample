import os
import pytest
import requests
import schemathesis
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".test.env")

@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    if not url:
        raise ValueError("BASE_URL not set in environment")
    return url

@pytest.fixture(scope="session")
def schema_url():
    url = os.getenv("SCHEMA")
    if not url:
        raise ValueError("SCHEMA not set in environment")
    return url

@pytest.fixture(scope="session")
def credentials():
    username = os.getenv("AUTH_USERNAME")
    password = os.getenv("AUTH_PASSWORD")
    if not username or not password:
        raise ValueError("AUTH_USERNAME and AUTH_PASSWORD must be set in environment")
    return {"username": username, "password": password}

@pytest.fixture(scope="session")
def schemathesis_schema(schema_url, base_url):
    schema = schemathesis.openapi.from_url(schema_url)
    schema.config.update(base_url=base_url)
    schema.config.checks.update(excluded_check_names=["unsupported_method"]) # Exclude checks for unsupported HTTP methods to simplify testing for now.
    schema.config.output.sanitization.update(enabled=False)
    return schema

@pytest.fixture(scope="session")
def auth_token(base_url, credentials):
    response = requests.post(
        f"{base_url}/auth",
        json=credentials
    )
    return response.json()["token"]


@pytest.fixture(scope="session")
def api_key():
    return os.getenv("API_KEY")


@pytest.fixture(scope="session")
def session(api_key):
    s = requests.Session()
    if api_key:
        s.headers.update({"Authorization": f"Bearer {api_key}"})
    s.headers.update({"Content-Type": "application/json"})
    return s
