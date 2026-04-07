from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import get_settings
from app.core.request_context import reset_request_identity, set_request_identity


def _extract_client_ip(request: Request) -> str | None:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


class RequestIdentityMiddleware(BaseHTTPMiddleware):
    """Store request identity context for outbound API forwarding headers."""

    async def dispatch(self, request: Request, call_next):
        client_ip = _extract_client_ip(request)
        user_agent = request.headers.get("user-agent")
        tokens = set_request_identity(client_ip=client_ip, user_agent=user_agent)
        try:
            return await call_next(request)
        finally:
            reset_request_identity(tokens)


class APIStatusMiddleware(BaseHTTPMiddleware):
    """Restrict non-overview API endpoints when API availability is disabled."""

    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        header_credit = settings.required_credit_line.replace("©", "(C)")
        path = request.url.path
        allowed_paths = {"/api", "/api/"}
        allowed_prefixes = (
            "/api/docs",
            "/api/openapi.json",
            "/api/redoc",
            "/api/docs/oauth2-redirect",
        )

        if not settings.api_availability and path.startswith("/api"):
            is_allowed = path in allowed_paths or any(
                path.startswith(prefix) for prefix in allowed_prefixes
            )
            if not is_allowed:
                now_iso = datetime.now(timezone.utc).isoformat()
                base_url = str(request.base_url).rstrip("/")
                payload = {
                    "success": False,
                    "status": {
                        "http_code": 503,
                        "code": "API_TEMPORARILY_UNAVAILABLE",
                        "message": (
                            "This endpoint is temporarily unavailable due to high "
                            "traffic and protection limits."
                        ),
                    },
                    "credit": settings.required_credit_line,
                    "request": {
                        "method": request.method,
                        "path": path,
                        "timestamp": now_iso,
                    },
                    "documentation": {
                        "overview": f"{base_url}/api/",
                        "swagger": f"{base_url}/api/docs",
                        "redoc": f"{base_url}/api/redoc",
                        "openapi": f"{base_url}/api/openapi.json",
                    },
                    "alternative_endpoints": [
                        {
                            "name": "High Availability Endpoint",
                            "url": "https://pddikti.fastapicloud.dev",
                            "description": (
                                "Alternative endpoint designed to remain available "
                                "during high traffic periods."
                            ),
                        }
                    ],
                    "support": {
                        "message": (
                            "If this issue persists, please check service status on "
                            "the overview endpoint and contact support."
                        ),
                        "live_chat": "https://ridwaanhall.com/guestbook",
                        "email": "hi@ridwaanhall.com",
                        "contact_form": "https://ridwaanhall.com/contact",
                    },
                    "retry_after_seconds": 3600,
                }
                return JSONResponse(
                    payload,
                    status_code=503,
                    headers={
                        "Retry-After": "3600",
                        "X-Project-Credit": header_credit,
                    },
                )

        return await call_next(request)


class SEOHeadersMiddleware(BaseHTTPMiddleware):
    """Add SEO and security headers to every response."""

    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        header_credit = settings.required_credit_line.replace("©", "(C)")
        response = await call_next(request)
        response.headers.setdefault("X-Robots-Tag", "index, follow")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        if request.url.path.startswith("/api"):
            response.headers.setdefault("X-Project-Credit", header_credit)
        return response
