from fastapi import APIRouter
from datetime import datetime, timezone

from app.api.common import settings


router = APIRouter(tags=["overview"])


@router.get(
    "/",
    summary="API overview",
    description="Return API metadata, service status, and support information.",
)
def api_overview():
    public_base_url = settings.public_base_url
    api_base_url = f"{public_base_url}/api"
    now_iso = datetime.now(timezone.utc).isoformat()

    documentation = {
        "overview": f"{api_base_url}/",
        "swagger": f"{api_base_url}/docs",
        "redoc": f"{api_base_url}/redoc",
        "openapi": f"{api_base_url}/openapi.json",
        "web_explorer": f"{public_base_url}/web",
    }

    support = {
        "live_chat": "https://ridwaanhall.com/guestbook",
        "email": "hi@ridwaanhall.com",
        "contact_form": "https://ridwaanhall.com/contact",
    }

    alternatives = [
        {
            "name": "High Availability Endpoint",
            "url": "https://pddikti.fastapicloud.dev",
            "description": "Alternative endpoint optimized for high traffic periods.",
        }
    ]

    service = {
        "name": "PDDikti Public Data API Web",
        "version": settings.api_version,
        "base_url": f"{api_base_url}/",
        "description": (
            "Structured public-data API for Indonesian higher education entities, "
            "including universities, study programs, lecturers, and students."
        ),
        "last_update": settings.last_update,
        "generated_at": now_iso,
    }

    if settings.api_availability:
        availability = {
            "state": "operational",
            "code": "SERVICE_AVAILABLE",
            "http_code": 200,
            "message": "API service is operational. All endpoints are available.",
            "limited_endpoints": [],
        }
    else:
        availability = {
            "state": "limited",
            "code": "SERVICE_LIMITED_HIGH_TRAFFIC",
            "http_code": 200,
            "message": (
                "Service is running in limited mode due to high traffic. "
                "Use this endpoint and documentation links for status and guidance."
            ),
            "limited_endpoints": [
                {
                    "scope": "Most /api endpoints except overview and documentation routes",
                    "response_code": 503,
                    "retry_after_seconds": 3600,
                }
            ],
        }

    return {
        "success": True,
        "status": {
            "http_code": 200,
            "code": "API_OVERVIEW_OK",
            "message": "API overview retrieved successfully.",
        },
        "credit": settings.required_credit_line,
        "service": service,
        "availability": availability,
        "documentation": documentation,
        "support": support,
        "alternative_endpoints": alternatives,
    }


ENDPOINT_GROUP = {
    "id": "overview",
    "label": "Overview",
    "description": "Service metadata and health context.",
    "endpoints": [
        {
            "method": "GET",
            "path": "/api/",
            "summary": "API overview",
        }
    ],
}
