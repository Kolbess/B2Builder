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
