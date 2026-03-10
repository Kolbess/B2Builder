from app.services.pdf_renderer import render_pdf
import pytest


def test_render_pdf_basic():
    # using the sample template that is committed in the repo
    data = {"title": "Hello", "content": "World"}
    pdf = render_pdf("invoice_standard", data)
    assert isinstance(pdf, (bytes, bytearray))
    assert pdf.startswith(b"%PDF-"), "output should start with PDF magic header"
    assert len(pdf) > 100, "PDF should not be empty"


def test_render_pdf_missing_template():
    with pytest.raises(Exception) as exc:
        render_pdf("no_such_template", {})
    # jinja2 throws TemplateNotFound
    assert "TemplateNotFound" in repr(exc.value)
