from pydantic import BaseModel, Field
from typing import Dict, Any, List


class InvoiceItem(BaseModel):
    description: str = Field(..., description="Nazwa pozycji lub opis towaru/usługi")
    quantity: int = Field(..., description="Ilość jednostek")
    unit_price: float = Field(..., description="Cena za jednostkę")
    total_price: float = Field(
        ...,
        description="Łączna cena pozycji (quantity * unit_price). Sprawdzana po stronie klienta lub szablonu."
    )


class InvoiceCustomer(BaseModel):
    name: str = Field(..., description="Imię lub nazwa klienta")
    address: str = Field(..., description="Adres klienta")


class InvoiceData(BaseModel):
    invoice_number: str = Field(..., description="Numer faktury")
    customer: InvoiceCustomer
    items: List[InvoiceItem]
    extras: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Opcjonalne dodatkowe tabele lub listy danych o dowolnej strukturze"
    )


class GenerateRequest(BaseModel):
    template_id: str = Field(
        description="Unikalny identyfikator szablonu dokumentu PDF, który ma zostać użyty do generowania. Przykładowe wartości: 'invoice_standard', 'certificate_custom', 'report_monthly'. Szablon określa strukturę i styl dokumentu wyjściowego."
    )
    data: Dict[str, Any] = Field(
        description="Obiekt JSON zawierający dane do wypełnienia szablonu. Struktura danych musi odpowiadać schematowi wybranego szablonu. Na przykład dla faktury: {'invoice_number': 'INV-001', 'customer': {'name': 'ABC Corp', 'address': '123 Main St'}, 'items': [...]}"
    )


class TemplateSchema(BaseModel):
    id: str = Field(description="Unikalny identyfikator szablonu")
    name: str = Field(description="Przyjazna nazwa szablonu")
    description: str = Field(description="Opis szablonu i jego zastosowania")
    example_request: Dict[str, Any] = Field(description="Przykładowe pełne żądanie JSON do skopiowania i wypełnienia dla tego szablonu")


class TemplatesResponse(BaseModel):
    templates: List[TemplateSchema] = Field(description="Lista dostępnych szablonów")
    examples: List[Dict[str, Any]] = Field(description="Lista przykładowych żądań JSON dla każdego szablonu")