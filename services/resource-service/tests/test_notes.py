import os

import jwt

os.environ["JWT_ACCESS_SECRET"] = "test-only-secret-for-resource-service-32-bytes"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
JWT_SECRET = os.environ["JWT_ACCESS_SECRET"]

def test_healthz():
    """Verify healthcheck endpoint returns status 200 and ok."""
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "resource-service"}

def test_unauthorized_access_returns_401():
    """Accessing protected endpoint without a token must return 401."""
    response = client.get('/notes/')
    assert response.status_code == 401

def test_invalid_token_returns_401():
    """Accessing protected endpoint with an invalid token must return 401."""
    response = client.get('/notes', headers={
        'Authorization': 'Bearer invalid.jwt.token'
    })  # Update to '/api/notes' if defined with /api prefix
    assert response.status_code == 401

def test_identity_headers_cannot_authenticate_an_admin_request():
    response = client.get('/resources/admin', headers={
        'X-User-Id': 'attacker',
        'X-User-Email': 'attacker@example.com',
        'X-User-Role': 'admin'
    })
    assert response.status_code == 401

def test_valid_admin_token_can_access_admin_endpoint():
    token = jwt.encode(
        {'sub': 'admin-user', 'email': 'admin@example.com', 'role': 'admin'},
        JWT_SECRET,
        algorithm='HS256'
    )
    response = client.get('/resources/admin', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200

def test_metrics_endpoint_exposes_http_metrics():
    client.get('/healthz')
    response = client.get('/metrics')

    assert response.status_code == 200
    assert 'http_requests_total' in response.text