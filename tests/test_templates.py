import os
import sys
# ensure the workspace root is on sys.path so `app` package is importable
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_templates():
    response = client.get("/v1/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert isinstance(data["templates"], list)
    assert len(data["templates"]) > 0
    # Check structure of first template
    template = data["templates"][0]
    assert "id" in template
    assert "name" in template
    assert "description" in template
    assert "example_request" in template
    # Ensure example_request is a dict/object
    assert isinstance(template["example_request"], dict)
    # Check that example_request has template_id and data
    assert "template_id" in template["example_request"]
    assert "data" in template["example_request"]

    # Also include top-level examples list for ease of copy/paste
    assert "examples" in data
    assert isinstance(data["examples"], list)
    assert len(data["examples"]) == len(data["templates"])