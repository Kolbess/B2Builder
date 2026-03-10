import os
import sys
# ensure workspace root on path for imports
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

# load .env if present
from dotenv import load_dotenv
load_dotenv()

from app.services.pdf_renderer import prepare_assets_css, render_pdf
import base64
import pytest


def test_prepare_assets_css_empty():
    assert prepare_assets_css({}) == ""


def test_prepare_assets_css_fonts():
    fake = "ZmFrZUZvbnREYXRh"  # 'fakeFontData' base64
    css = prepare_assets_css({"fonts": {"MyFont": fake}})
    assert "@font-face" in css
    assert "MyFont" in css
    assert fake in css


def test_render_pdf_with_logo(tmp_path, monkeypatch):
    # logo is just a tiny 1x1 png base64
    one_px = base64.b64encode(b"\x89PNG\r\n\x1a\n").decode()
    data = {"title": "A", "content": "B", "assets": {"logo": f"data:image/png;base64,{one_px}"}}
    pdf = render_pdf("invoice_standard", data)
    assert pdf.startswith(b"%PDF-"), "should still produce a PDF"


def test_render_pdf_with_font(tmp_path):
    fake = base64.b64encode(b"dummy").decode()
    assets = {"fonts": {"X": fake}}
    data = {"title": "A", "content": "B", "assets": assets}
    pdf = render_pdf("invoice_standard", data)
    assert pdf.startswith(b"%PDF-")
