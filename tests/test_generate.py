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
        "/v1/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={
            "template_id": "invoice_standard",
            "data": {
                "invoice_number": "INV-001",
                "customer": {"name": "ABC Corp", "address": "123 Main St"},
                "items": [{"description": "Product A", "quantity": 2, "unit_price": 10.0, "total_price": 20.0}]
            }
        }
    )
    assert response.status_code == 200
    # should be a PDF stream
    assert response.headers.get("content-type") == "application/pdf"
    # ensure download header is present
    assert "attachment" in response.headers.get("content-disposition", "")
    assert response.content.startswith(b"%PDF-")


def test_generate_missing_template_id():
    response = client.post(
        "/v1/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={"data": {"key": "value"}}
    )
    assert response.status_code == 422
    body = response.json()
    assert "template_id" in str(body)


def test_generate_missing_data():
    response = client.post(
        "/v1/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={"template_id": "invoice_standard"}
    )
    assert response.status_code == 422
    body = response.json()
    assert "data" in str(body)


def test_generate_invalid_data_type():
    response = client.post(
        "/v1/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={"template_id": "invoice_standard", "data": "not a dict"}
    )
    assert response.status_code == 422
    body = response.json()
    # the exact validation message may vary by Pydantic version
    text = str(body)
    assert "Input should be a valid dictionary" in text or "dict_type" in text or "type_error.dict" in text


def test_generate_certificate_custom():
    response = client.post(
        "/v1/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={
            "template_id": "certificate_custom",
            "data": {
                "recipient_name": "Jan Kowalski",
                "course_title": "Python Advanced",
                "completion_date": "2026-03-17",
                "issuer_name": "B2Builder Academy",
                "certificate_number": "CERT-2026-001"
            }
        }
    )
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/pdf"
    assert response.content.startswith(b"%PDF-")


def test_generate_report_monthly():
    response = client.post(
        "/v1/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={
            "template_id": "report_monthly",
            "data": {
                "report_title": "Monthly Report March 2026",
                "report_month": "2026-03",
                "summary": "Summary of business activities",
                "metrics": {
                    "revenue": 15000.0,
                    "expenses": 12000.0,
                    "profit": 3000.0
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/pdf"
    assert response.content.startswith(b"%PDF-")
