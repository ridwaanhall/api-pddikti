from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.router import API_ENDPOINT_CATALOG, iter_all_api_endpoints
from app.core.config import get_settings


router = APIRouter(tags=["web"])
settings = get_settings()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def _iter_static_api_paths() -> list[str]:
    return sorted(
        {
            endpoint["path"]
            for endpoint in iter_all_api_endpoints()
            if "{" not in endpoint["path"]
        }
    )


@router.get("/")
def landing_page(request: Request):
    context = {
        "active_page": "landing",
        "project_name": "PDDIKTI API",
        "api_version": settings.api_version,
        "api_available": settings.api_availability,
        "last_updated": settings.last_update,
    }
    return templates.TemplateResponse(request, "landing.html", context)


@router.get("/web")
def web_api_reference(request: Request):
    context = {
        "active_page": "web",
        "project_name": "PDDIKTI API",
        "endpoint_groups": API_ENDPOINT_CATALOG,
        "total_endpoints": len(iter_all_api_endpoints()),
    }
    return templates.TemplateResponse(request, "web_api.html", context)


@router.get("/robots.txt")
def robots_txt():
    base_url = "https://api-pddikti.rone.dev"
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow:",
        "",
        f"Sitemap: {base_url}/sitemap.xml",
    ]
    return PlainTextResponse("\n".join(lines), media_type="text/plain; charset=utf-8")


@router.get("/sitemap.xml")
def sitemap_xml():
    base_url = "https://api-pddikti.rone.dev"
    lastmod = settings.last_update.split("T")[0]

    static_urls = [
        ("/", "1.0", "daily"),
        ("/web", "0.9", "daily"),
        ("/api/", "0.9", "daily"),
        ("/api/docs", "0.7", "weekly"),
    ]

    for path in _iter_static_api_paths():
        if path not in {"/api/"}:
            static_urls.append((path, "0.7", "weekly"))

    url_entries = []
    for path, priority, changefreq in static_urls:
        url_entries.append(
            f"  <url>\n"
            f"    <loc>{base_url}{path}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_entries)
        + "\n</urlset>"
    )
    return Response(content=xml, media_type="application/xml; charset=utf-8")
