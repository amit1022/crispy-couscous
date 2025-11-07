import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

ACTIVITY = "Chess Club"
EMAIL = "testuser@mergington.edu"


def test_signup_for_activity():
    # Remove if already present
    client.delete(f"/activities/{ACTIVITY}/unregister?email={EMAIL}")
    # Sign up
    resp = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert resp.status_code == 200
    assert f"Signed up {EMAIL}" in resp.json()["message"]
    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert resp2.status_code == 400
    assert "already signed up" in resp2.json()["detail"]


def test_unregister_from_activity():
    # Ensure present
    client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    # Unregister
    resp = client.delete(f"/activities/{ACTIVITY}/unregister?email={EMAIL}")
    assert resp.status_code == 200
    assert f"Unregistered {EMAIL}" in resp.json()["message"]
    # Unregister again should fail
    resp2 = client.delete(f"/activities/{ACTIVITY}/unregister?email={EMAIL}")
    assert resp2.status_code == 404
    assert "not found" in resp2.json()["detail"]
