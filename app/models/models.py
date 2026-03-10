from pydantic import BaseModel, Field
from typing import Dict, Any

class GenerateRequest(BaseModel):
    template_id: str = Field(description="Unikalny identyfikator szablonu dokumentu PDF, który ma zostać użyty do generowania. Przykładowe wartości: 'invoice_standard', 'certificate_custom', 'report_monthly'. Szablon określa strukturę i styl dokumentu wyjściowego.")
    data: Dict[str, Any] = Field(description="Obiekt JSON zawierający dane do wypełnienia szablonu. Struktura danych musi odpowiadać schematowi wybranego szablonu. Na przykład dla faktury: {'invoice_number': 'INV-001', 'customer': {'name': 'ABC Corp', 'address': '123 Main St'}, 'items': [...]}")