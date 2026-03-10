from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

# load from .env if present (python-dotenv is in requirements)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Default secret for testing, should be overridden by environment variable
VALID_API_KEY = os.getenv("API_KEY", "secret-key-123")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == VALID_API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
