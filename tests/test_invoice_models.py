import os
import sys
# ensure the workspace root is on sys.path so `app` package is importable
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from pydantic import ValidationError
from app.models.models import InvoiceItem, InvoiceCustomer, InvoiceData


def test_invoice_item_valid():
    item = InvoiceItem(
        description="Product A",
        quantity=2,
        unit_price=10.0,
        total_price=20.0,
    )
    assert item.quantity == 2
    assert item.total_price == item.quantity * item.unit_price


def test_invoice_item_missing_field():
    try:
        InvoiceItem(description="Product B", quantity=1, unit_price=5.0)
        assert False, "ValidationError expected"
    except ValidationError as exc:
        assert "total_price" in str(exc)


def test_invoice_customer_valid():
    cust = InvoiceCustomer(name="ABC Corp", address="123 Main St")
    assert cust.name == "ABC Corp"


def test_invoice_data_valid():
    cust = InvoiceCustomer(name="ABC Corp", address="123 Main St")
    item = InvoiceItem(description="Product A", quantity=1, unit_price=15.0, total_price=15.0)
    data = InvoiceData(invoice_number="INV-001", customer=cust, items=[item])
    assert data.invoice_number == "INV-001"
    assert len(data.items) == 1


def test_invoice_data_wrong_items_type():
    try:
        InvoiceData(invoice_number="INV-002", customer={"name": "X", "address": "Y"}, items="not a list")
        assert False, "ValidationError expected"
    except ValidationError as exc:
        assert "items" in str(exc)
