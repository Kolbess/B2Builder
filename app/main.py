from fastapi import FastAPI
from app.models import GenerateRequest

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
