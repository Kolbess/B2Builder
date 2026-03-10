import os
import sys
# ensure the workspace root is on sys.path so `app` package is importable
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

# ensure any local .env is read before importing app
from dotenv import load_dotenv
load_dotenv()

from fastapi.testclient import TestClient
from app.main import app
from app.core.security import VALID_API_KEY

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_without_api_key():
    response = client.post(
        "/generate",
        json={"template_id": "invoice_standard", "data": {"key": "value"}}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API Key"}

def test_generate_with_invalid_api_key():
    response = client.post(
        "/generate",
        headers={"X-API-KEY": "invalid-key"},
        json={"template_id": "invoice_standard", "data": {"key": "value"}}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API Key"}

def test_generate_with_valid_api_key():
    response = client.post(
        "/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={"template_id": "invoice_standard", "data": {"key": "value"}}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success", "template_id": "invoice_standard", "message": "Authenticated"}
