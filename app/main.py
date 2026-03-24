from fastapi import FastAPI
from app.models import GenerateRequest, TemplateSchema, TemplatesResponse

app = FastAPI(
    title="B2Builder API",
    description="SaaS API for PDF generation"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root_redirect():
    """Convenience route: redirect the browser to the interactive docs."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

from fastapi import Depends
from fastapi.responses import StreamingResponse
import io

from app.core.security import get_api_key
from app.services.pdf_renderer import render_pdf

@app.post(
    "/v1/generate",
    dependencies=[Depends(get_api_key)],
    responses={200: {"content": {"application/pdf": {}}}},
    summary="Generuj dokument PDF",
    description="Utwórz dokument PDF na podstawie wybranego szablonu i dostarczonych danych. Wybierz szablon z listy dostępnych (GET /v1/templates), przygotuj dane zgodnie z przykładem i wyślij żądanie. Dokument zostanie zwrócony jako plik do pobrania.",
    tags=["Generowanie PDF"]
)
def generate_pdf(request: GenerateRequest):
    """Generate a PDF from a template and return it as a binary stream.

    The response includes a ``Content-Disposition`` header so that browsers
    and the Swagger UI offer a download rather than trying to render the raw
    bytes as text.
    """
    pdf_bytes = render_pdf(request.template_id, request.data)
    headers = {"Content-Disposition": "attachment; filename=generated.pdf"}
    return StreamingResponse(
        io.BytesIO(pdf_bytes), media_type="application/pdf", headers=headers
    )


@app.get("/v1/templates",
          summary="Pobierz dostępne szablony",
          description="Zwróć listę wszystkich dostępnych szablonów dokumentów PDF wraz z przykładami żądań, które można skopiować i dostosować. Każdy szablon zawiera unikalny identyfikator, nazwę, opis oraz przykładowe dane JSON do użycia w żądaniu POST /v1/generate.",
          tags=["Szablony"],
          response_model=TemplatesResponse)
def get_templates():
    """
    Zwraca listę wszystkich dostępnych szablonów dokumentów PDF z przykładowymi żądaniami.
    """
    templates = [
        TemplateSchema(
            id="invoice_standard",
            name="Standardowa Faktura",
            description="Szablon dla standardowych faktur z pozycjami i danymi klienta.",
            example_request={
                "template_id": "invoice_standard",
                "data": {
                    "invoice_number": "INV-001",
                    "customer": {"name": "ABC Corp", "address": "123 Main St"},
                    "items": [
                        {
                            "description": "Product A",
                            "quantity": 2,
                            "unit_price": 10.0,
                            "total_price": 20.0
                        }
                    ]
                }
            }
        ),
        TemplateSchema(
            id="certificate_custom",
            name="Certyfikat Niestandardowy",
            description="Szablon dla certyfikatów z możliwością dostosowania.",
            example_request={
                "template_id": "certificate_custom",
                "data": {
                    "recipient_name": "Jan Kowalski",
                    "course_title": "Python Advanced",
                    "completion_date": "2026-03-17",
                    "issuer_name": "B2Builder Academy",
                    "certificate_number": "CERT-2026-001"
                }
            }
        ),
        TemplateSchema(
            id="report_monthly",
            name="Raport Miesięczny",
            description="Szablon dla miesięcznych raportów biznesowych.",
            example_request={
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
    ]

    examples = [t.example_request for t in templates]

    return TemplatesResponse(templates=templates, examples=examples)
