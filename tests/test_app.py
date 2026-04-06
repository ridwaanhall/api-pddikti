from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_landing_page_works() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Option 1" in response.text
    assert "Option 2" in response.text


def test_api_overview_works() -> None:
    response = client.get("/api/")
    assert response.status_code == 200
    payload = response.json()
    assert "meta" in payload
    assert "status" in payload


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
    assert "Route Explorer" in response.text
    assert "Search Routes" in response.text


def test_web_group_page_works() -> None:
    response = client.get("/web/routes/dosen")
    assert response.status_code == 200
    assert "Dosen Routes" in response.text
    assert "Get lecturer profile" in response.text


def test_web_proxy_overview_works() -> None:
    response = client.get("/web/api-overview/")
    assert response.status_code == 200
    payload = response.json()
    assert "meta" in payload
