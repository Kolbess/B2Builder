from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="B2Builder API",
    description="SaaS API for PDF generation"
)

class GenerateRequest(BaseModel):
    template_id: str = Field(..., description="ID szablonu, np. 'invoice_standard'")
    data: dict = Field(..., description="Dane JSON pasujące do schematu wybranego szablonu")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root_redirect():
    """Convenience route: redirect the browser to the interactive docs."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

from fastapi import Depends
from app.core.security import get_api_key

@app.post("/generate", dependencies=[Depends(get_api_key)])
def generate_pdf(request: GenerateRequest):
    return {"status": "success", "template_id": request.template_id, "message": "Authenticated"}
