from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


client = TestClient(app)
settings = get_settings()

REQUIRED_CREDIT = settings.required_credit_line


def test_landing_page_works() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Open Web Playground" in response.text
    assert "Swagger Docs" in response.text
    assert settings.brand_name in response.text
    assert settings.maintainer in response.text
    # Non-affiliation notice must be present on the public landing page.
    assert "Not affiliated with" in response.text


def test_api_overview_works() -> None:
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.headers.get("X-Project-Credit")
    assert settings.brand_name in response.headers.get("X-Project-Credit", "")
    payload = response.json()
    assert payload.get("success") is True
    assert payload.get("credit") == REQUIRED_CREDIT
    assert "service" in payload
    assert "availability" in payload
    assert "documentation" in payload
    assert "support" in payload
    assert "alternative_endpoints" in payload
    assert payload.get("disclaimer")
    assert "not affiliated" in payload["disclaimer"].lower()


def test_blocked_api_response_includes_credit_header() -> None:
    response = client.get("/api/search/all/informatika/")
    if response.status_code == 503:
        assert response.headers.get("X-Project-Credit")
        assert settings.brand_name in response.headers.get("X-Project-Credit", "")
        payload = response.json()
        assert payload.get("success") is False
        assert payload.get("status", {}).get("code") == "API_TEMPORARILY_UNAVAILABLE"
        assert "documentation" in payload
        assert "support" in payload
        assert "alternative_endpoints" in payload


def test_api_docs_works() -> None:
    response = client.get("/api/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_api_redoc_works() -> None:
    response = client.get("/api/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text.lower()


def test_web_api_page_works() -> None:
    response = client.get("/web")
    assert response.status_code == 200
    assert "Routes" in response.text
    assert "Execute" in response.text
    assert "Snippet" in response.text


def test_web_group_page_works() -> None:
    response = client.get("/web/routes/dosen")
    assert response.status_code == 200
    assert "Lecturers (Dosen)" in response.text
    assert "Get lecturer profile" in response.text


def test_web_proxy_overview_works() -> None:
    response = client.get("/web/api-overview/")
    assert response.status_code == 200
    payload = response.json()
    assert "service" in payload
