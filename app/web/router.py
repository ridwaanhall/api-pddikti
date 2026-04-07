from pathlib import Path
import re
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.router import API_ENDPOINT_CATALOG
from app.core.config import get_settings


router = APIRouter(tags=["web"])
settings = get_settings()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def _group_label(group_key: str) -> str:
    mapping = {
        "overview": "Overview Routes",
        "search": "Search Routes",
        "pt": "PT Routes",
        "prodi": "Prodi Routes",
        "dosen": "Dosen Routes",
        "mhs": "Mahasiswa Routes",
        "stats": "Statistics Routes",
        "prodi-bidang-ilmu": "Prodi Bidang Ilmu Routes",
    }
    return mapping.get(group_key, f"{group_key.replace('-', ' ').title()} Routes")


def _group_description(group_key: str) -> str:
    mapping = {
        "overview": "Metadata and health information for the API service.",
        "search": "Search endpoints across universities, programs, lecturers, and students.",
        "pt": "University-focused endpoints including profile, metrics, and assets.",
        "prodi": "Study-program focused endpoints with profile and metrics data.",
        "dosen": "Lecturer profile, history, and portfolio endpoints.",
        "mhs": "Student profile and status endpoints.",
        "stats": "Aggregate statistics grouped by various dimensions.",
        "prodi-bidang-ilmu": "Study-program categories grouped by scientific field.",
    }
    return mapping.get(group_key, "Grouped API endpoints.")


def _make_operation_id(path: str, method: str, fallback: str | None) -> str:
    raw = fallback or f"{method}-{path}"
    normalized = re.sub(r"[^a-zA-Z0-9_-]", "-", raw).strip("-")
    return normalized.lower()


def _web_path_from_api_path(api_path: str) -> str:
    if api_path == "/api/":
        return "/web/api-overview/"
    suffix = api_path[len("/api") :]
    return f"/web{suffix}"


def _collect_web_docs(request: Request) -> tuple[list[dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    schema = request.app.openapi()
    path_lookup: dict[tuple[str, str], dict[str, Any]] = {}
    lookup: dict[tuple[str, str], dict[str, Any]] = {}

    for api_path, methods in schema.get("paths", {}).items():
        if not api_path.startswith("/api"):
            continue
        if api_path in {"/api/openapi.json", "/api/docs", "/api/redoc"}:
            continue

        for http_method, operation in methods.items():
            path_lookup[(http_method.upper(), api_path)] = operation

    groups: list[dict[str, Any]] = []
    for catalog_group in API_ENDPOINT_CATALOG:
        if catalog_group.get("id") == "overview":
            continue

        endpoints = catalog_group.get("endpoints", [])
        route_key = "overview"
        if endpoints:
            first_path = endpoints[0]["path"].removeprefix("/api/").strip("/")
            route_key = first_path.split("/")[0] if first_path else "overview"

        operations: list[dict[str, Any]] = []
        for endpoint in endpoints:
            method = endpoint["method"].upper()
            api_path = endpoint["path"]
            operation = path_lookup.get((method, api_path), {})

            parameters = []
            for parameter in operation.get("parameters", []):
                schema_info = parameter.get("schema", {})
                parameters.append(
                    {
                        "name": parameter.get("name", ""),
                        "in": parameter.get("in", "path"),
                        "required": parameter.get("required", False),
                        "type": schema_info.get("type", "string"),
                        "title": schema_info.get(
                            "title",
                            parameter.get("name", "parameter").replace("_", " ").title(),
                        ),
                        "default": schema_info.get("default", ""),
                        "enum": schema_info.get("enum", []),
                        "description": parameter.get("description", "No description provided."),
                    }
                )

            request_body = None
            body_schema = (
                operation.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            if body_schema:
                request_body = {
                    "required": operation.get("requestBody", {}).get("required", False),
                    "schema": body_schema,
                }

            operation_id = _make_operation_id(api_path, method, operation.get("operationId"))
            operation_detail = {
                "id": operation_id,
                "method": method,
                "summary": operation.get("summary") or endpoint.get("summary") or "Unnamed endpoint",
                "description": operation.get("description") or "No description provided.",
                "api_path": api_path,
                "web_path": _web_path_from_api_path(api_path),
                "parameters": parameters,
                "request_body": request_body,
            }

            operations.append(operation_detail)
            lookup[(route_key, operation_id)] = operation_detail

        groups.append(
            {
                "id": catalog_group.get("id", route_key),
                "key": route_key,
                "label": catalog_group.get("label") or _group_label(route_key),
                "description": catalog_group.get("description") or _group_description(route_key),
                "operations": operations,
            }
        )

    return groups, lookup


def _resolve_selected_group(
    groups: list[dict[str, Any]],
    requested_group: str | None,
) -> dict[str, Any]:
    available_groups = [group for group in groups if group["operations"]]
    if not available_groups:
        raise HTTPException(status_code=500, detail="No web operations found")

    default_group = next((group for group in available_groups if group["key"] == "search"), available_groups[0])
    if not requested_group:
        return default_group
    return next(
        (group for group in available_groups if group["key"] == requested_group),
        default_group,
    )


def _resolve_selected_operation(
    selected_group: dict[str, Any],
    requested_operation: str | None,
) -> dict[str, Any] | None:
    operations = selected_group.get("operations", [])
    if not operations:
        return None
    if not requested_operation:
        return None
    return next((operation for operation in operations if operation["id"] == requested_operation), None)


def _build_web_context(
    request: Request,
    group: str | None = None,
    operation: str | None = None,
    view: str | None = None,
) -> dict[str, Any]:
    current_base_url = str(request.base_url).rstrip("/")
    groups, _ = _collect_web_docs(request)
    selected_group = _resolve_selected_group(groups, group)
    selected_operation = _resolve_selected_operation(selected_group, operation)

    is_single_view = view == "single" and selected_operation is not None
    rendered_operations = [selected_operation] if is_single_view else selected_group["operations"]

    return {
        "request": request,
        "active_page": "web",
        "project_name": "PDDikti API",
        "public_base_url": current_base_url,
        "groups": groups,
        "selected_group": selected_group,
        "selected_operation": selected_operation,
        "is_single_view": is_single_view,
        "rendered_operations": rendered_operations,
        "public_api_base_url": f"{current_base_url}/api",
        "total_endpoints": sum(len(group_item["operations"]) for group_item in groups),
    }


@router.get("/")
def landing_page(request: Request):
    current_base_url = str(request.base_url).rstrip("/")
    context = {
        "request": request,
        "active_page": "landing",
        "project_name": "PDDikti API",
        "public_base_url": current_base_url,
        "api_version": settings.api_version,
        "api_available": settings.api_availability,
        "last_updated": settings.last_update,
    }
    return templates.TemplateResponse(request, "landing.html", context)


@router.get("/web")
@router.get("/web/")
def web_api_home(
    request: Request,
    group: str | None = None,
    operation: str | None = None,
    view: str | None = None,
):
    context = _build_web_context(
        request=request,
        group=group,
        operation=operation,
        view=view,
    )
    return templates.TemplateResponse(request, "web_index.html", context)


@router.get("/web/routes/{group_key}")
def web_group_routes(request: Request, group_key: str):
    groups, _ = _collect_web_docs(request)
    selected_group = next((item for item in groups if item["key"] == group_key and item["operations"]), None)
    if not selected_group:
        raise HTTPException(status_code=404, detail="Route group not found")

    context = _build_web_context(request=request, group=selected_group["key"])
    return templates.TemplateResponse(request, "web_index.html", context)


@router.get("/web/routes/{group_key}/{operation_id}")
def web_route_detail(request: Request, group_key: str, operation_id: str):
    groups, lookup = _collect_web_docs(request)
    selected_group = next((item for item in groups if item["key"] == group_key and item["operations"]), None)
    if not selected_group:
        raise HTTPException(status_code=404, detail="Route detail not found")

    if not lookup.get((group_key, operation_id)):
        raise HTTPException(status_code=404, detail="Route detail not found")

    context = _build_web_context(
        request=request,
        group=selected_group["key"],
        operation=operation_id,
        view="single",
    )
    return templates.TemplateResponse(request, "web_index.html", context)


@router.get("/web/{forward_path:path}", include_in_schema=False)
async def web_api_proxy(request: Request, forward_path: str):
    normalized = forward_path.strip("/")
    if normalized.startswith("routes"):
        raise HTTPException(status_code=404, detail="Not Found")

    if normalized in {"", "web"}:
        raise HTTPException(status_code=404, detail="Not Found")

    api_target = "/api/" if normalized in {"api-overview", "api-overview/"} else f"/api/{forward_path}"

    transport = httpx.ASGITransport(app=request.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://local") as client:
        proxied = await client.get(api_target, params=request.query_params)

    passthrough_headers = {
        key: value
        for key, value in proxied.headers.items()
        if key.lower() not in {"content-length", "transfer-encoding", "connection"}
    }

    return Response(
        content=proxied.content,
        status_code=proxied.status_code,
        headers=passthrough_headers,
        media_type=proxied.headers.get("content-type"),
    )


@router.get("/robots.txt")
def robots_txt():
    base_url = settings.public_base_url
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow:",
        "",
        f"Sitemap: {base_url}/sitemap.xml",
    ]
    return PlainTextResponse("\n".join(lines), media_type="text/plain; charset=utf-8")


@router.get("/sitemap.xml")
def sitemap_xml(request: Request):
    base_url = settings.public_base_url
    lastmod = settings.last_update.split("T")[0]
    groups, _ = _collect_web_docs(request)

    static_urls = [
        ("/", "1.0", "daily"),
        ("/web", "0.9", "daily"),
        ("/api/", "0.9", "daily"),
        ("/api/docs", "0.7", "weekly"),
        ("/api/redoc", "0.7", "weekly"),
    ]

    for group in groups:
        static_urls.append((f"/web/routes/{group['key']}", "0.8", "weekly"))
        for operation in group["operations"]:
            static_urls.append(
                (
                    f"/web/routes/{group['key']}/{operation['id']}",
                    "0.7",
                    "weekly",
                )
            )
            if "{" not in operation["api_path"]:
                static_urls.append((operation["web_path"], "0.7", "weekly"))

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
