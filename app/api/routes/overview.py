from fastapi import APIRouter

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

    meta = {
        "base_url": f"{api_base_url}/",
        "version": {
            "current": settings.api_version,
            "minimum_supported": settings.api_version,
        },
        "description": (
            "Provides structured access to data from Pangkalan Data Pendidikan Tinggi "
            "(PDDikti), Indonesia's Higher Education Database"
        ),
        "last_updated": settings.last_update,
        "author": "ridwaanhall",
    }
    resources = {
        "api_docs": f"{api_base_url}/docs",
        "api_redoc": f"{api_base_url}/redoc",
        "api_root": f"{api_base_url}/",
        "web_explorer": f"{public_base_url}/web",
        "official_website": "https://pddikti.kemdiktisaintek.go.id/",
    }
    features = {
        "documentation": (
            "Comprehensive API guide with endpoints, examples, and usage instructions"
        ),
        "status_monitoring": "Real-time performance and availability tracking",
        "traffic_management": (
            "Automated request balancing and throttling for high availability"
        ),
    }

    if settings.api_availability:
        status = {
            "status": "Operational",
            "code": "OK_200",
            "severity": "normal",
            "message": "All endpoints are functioning normally.",
        }
        notice = {
            "headline": "Service Operational",
            "details": "Traffic levels have normalized and full services are restored.",
            "estimated_resolution": None,
            "support_contact": {
                "live_chat": "https://ridwaanhall.com/guestbook",
                "email": "hi@ridwaanhall.com",
                "form": "https://ridwaanhall.com/contact",
            },
        }
    else:
        status = {
            "status": "Limited Service",
            "code": "TRAFFIC_LIMIT_001",
            "severity": "warning",
            "message": "Some endpoints are temporarily unavailable due to high traffic",
        }
        notice = {
            "headline": "High Traffic Alert",
            "details": "To maintain stability, some services are temporarily limited.",
            "estimated_resolution": (
                "Expected recovery as traffic normalizes within days or weeks"
            ),
            "blog": (
                "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-"
                "mlbb-stats-and-api-pddikti/"
            ),
            "support_contact": {
                "live_chat": "https://ridwaanhall.com/guestbook",
                "email": "hi@ridwaanhall.com",
                "form": "https://ridwaanhall.com/contact",
            },
        }
        meta[
            "description"
        ] += ", covering universities, study programs, lecturers, and students."

    return {
        "credit": settings.required_credit_line,
        "meta": meta,
        "resources": resources,
        "features": features,
        "status": status,
        "notice": notice,
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
