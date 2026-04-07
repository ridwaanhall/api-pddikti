from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


REQUIRED_CREDIT = (
    "Powered by PDDikti Public Data API Web, Data © PDDikti, "
    "API maintained by ridwaanhall / RoneAI"
)


def test_landing_page_works() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Open Web Playground" in response.text
    assert "Open Swagger Docs" in response.text
    assert REQUIRED_CREDIT in response.text


def test_api_overview_works() -> None:
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.headers.get("X-Project-Credit")
    assert "Powered by PDDikti Public Data API Web" in response.headers.get(
        "X-Project-Credit", ""
    )
    payload = response.json()
    assert payload.get("credit") == REQUIRED_CREDIT
    assert "meta" in payload
    assert "status" in payload


def test_blocked_api_response_includes_credit_header() -> None:
    response = client.get("/api/search/all/informatika/")
    if response.status_code == 503:
        assert response.headers.get("X-Project-Credit")
        assert "Powered by PDDikti Public Data API Web" in response.headers.get(
            "X-Project-Credit", ""
        )


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
    assert "Web Playground" in response.text
    assert "Search all entities" in response.text
    assert "/web/search/all/{keyword}/" in response.text
    assert "Overview" not in response.text


def test_web_group_page_works() -> None:
    response = client.get("/web/routes/dosen")
    assert response.status_code == 200
    assert "Lecturers (Dosen)" in response.text
    assert "Get lecturer profile" in response.text


def test_web_proxy_overview_works() -> None:
    response = client.get("/web/api-overview/")
    assert response.status_code == 200
    payload = response.json()
    assert "meta" in payload
