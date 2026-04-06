from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_landing_page_works() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "PDDIKTI API" in response.text


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


def test_web_api_page_works() -> None:
    response = client.get("/web")
    assert response.status_code == 200
    assert "Web API Reference" in response.text
    assert "/api/search/all/{keyword}/" in response.text
