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

@app.post("/generate", dependencies=[Depends(get_api_key)])
def generate_pdf(request: GenerateRequest):
    """Generate a PDF from a template and return it as a binary stream."""
    pdf_bytes = render_pdf(request.template_id, request.data)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf")
