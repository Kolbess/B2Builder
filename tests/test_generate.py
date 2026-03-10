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


def test_generate_success():
    response = client.post(
        "/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={"template_id": "invoice_standard", "data": {"key": "value"}}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["template_id"] == "invoice_standard"


def test_generate_missing_template_id():
    response = client.post(
        "/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={"data": {"key": "value"}}
    )
    assert response.status_code == 422
    body = response.json()
    assert "template_id" in str(body)


def test_generate_missing_data():
    response = client.post(
        "/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={"template_id": "invoice_standard"}
    )
    assert response.status_code == 422
    body = response.json()
    assert "data" in str(body)


def test_generate_invalid_data_type():
    response = client.post(
        "/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={"template_id": "invoice_standard", "data": "not a dict"}
    )
    assert response.status_code == 422
    body = response.json()
    # the exact validation message may vary by Pydantic version
    text = str(body)
    assert "Input should be a valid dictionary" in text or "dict_type" in text or "type_error.dict" in text
