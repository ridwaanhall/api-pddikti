from fastapi.responses import JSONResponse
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
                payload = {
                    "error": "Service Temporarily Limited",
                    "message": (
                        "Due to high traffic volume, this endpoint is temporarily "
                        "unavailable to ensure system stability."
                        "use alternative endpoint or check back later."
                    ),
                    "code": 503,
                    "status": "Service Unavailable",
                    "alternative_endpoint": {
                        "always_online": "https://pddikti.fastapicloud.dev",
                        "description": (
                            "This alternative API endpoint is designed to remain "
                            "operational even during high traffic periods, providing "
                            "access to essential data with optimized performance."
                        ),
                    },
                    "available_endpoint": {
                        "url": str(request.base_url),
                        "method": "GET",
                        "description": (
                            "API Overview - Current service status and available resources"
                        ),
                    },
                    "support": {
                        "retry_suggestion": (
                            "Please try again in a few days (or weeks) as we are "
                            "currently experiencing high traffic."
                        ),
                        "support_message": (
                            "You can support us by donating from $1 USD (target: "
                            "$500 USD) to help enhance API performance and handle "
                            "high request volumes."
                        ),
                        "contact": "Contact support if this issue persists",
                        "contact_site": "https://ridwaanhall.com/guestbook",
                    },
                }
                return JSONResponse(payload, status_code=503, headers={"Retry-After": "3600"})

        return await call_next(request)


class SEOHeadersMiddleware(BaseHTTPMiddleware):
    """Add SEO and security headers to every response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Robots-Tag", "index, follow")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        return response
