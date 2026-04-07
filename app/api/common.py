from typing import Any

from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.services.api_client import APIClient


settings = get_settings()
api_client = APIClient()


def as_json(data: Any) -> Any:
    if isinstance(data, dict):
        data.setdefault("credit", settings.required_credit_line)

    if isinstance(data, dict) and isinstance(data.get("code"), int) and data["code"] >= 400:
        return JSONResponse(content=data, status_code=data["code"])
    return data
