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
from app.core.security import get_api_key

@app.post("/generate", dependencies=[Depends(get_api_key)])
def generate_pdf(request: GenerateRequest):
    return {"status": "success", "template_id": request.template_id, "message": "Authenticated"}
