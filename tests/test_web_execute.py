"""Tests for the playground's opaque execution endpoint.

The point of POST /web/execute is that whatever a user types stays in the request body
and never reaches a URL. These tests pin that behaviour plus the catalog guard that keeps
the endpoint from becoming an open proxy.
"""

from typing import Any
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest

from app.main import app


client = TestClient(app)


def _operation_ids(group: str) -> list[str]:
    import re

    page = client.get(f"/web/routes/{group}").text
    return re.findall(r'data-operation-id="([^"]+)"', page)


@pytest.fixture
def upstream():
    """Stub the outbound client so these tests never touch the network."""
    with patch("app.api.common.api_client._make_request") as mock:
        mock.return_value = {"status": "success", "data": [{"id": "abc==", "nama": "UGM"}]}
        yield mock


def test_playground_page_serves_cards_and_script() -> None:
    response = client.get("/web/routes/search")
    assert response.status_code == 200
    assert "data-endpoint-card" in response.text
    assert "/static/playground.js" in response.text
    assert "playground-config" in response.text


def test_static_playground_script_is_served() -> None:
    response = client.get("/static/playground.js")
    assert response.status_code == 200
    assert "web/execute" in response.text


def test_execute_sends_value_in_body_not_url(upstream) -> None:
    operation_id = next(oid for oid in _operation_ids("search") if "search_pt" in oid)

    response = client.post(
        "/web/execute",
        json={
            "operation_id": operation_id,
            "group": "search",
            "params": {"keyword": "gadjah mada"},
        },
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["nama"] == "UGM"
    # The request line carries no user input at all.
    assert response.request.url.path == "/web/execute"
    assert "gadjah" not in str(response.request.url)
    # ...but it did reach the upstream client.
    assert "gadjah%20mada" in upstream.call_args.args[0]


def test_execute_preserves_base64_padding_in_ids(upstream) -> None:
    operation_id = next(oid for oid in _operation_ids("pt") if "pt_detail" in oid)
    entity_id = "muM28NSb_I4rz-obNKpgpKA=="

    response = client.post(
        "/web/execute",
        json={"operation_id": operation_id, "group": "pt", "params": {"id_pt": entity_id}},
    )

    assert response.status_code == 200
    # '=' must survive the whole round trip or upstream answers 400 invalid id.
    assert upstream.call_args.args[0].endswith(entity_id)


def test_execute_rejects_unknown_operation() -> None:
    response = client.post(
        "/web/execute", json={"operation_id": "not-a-real-operation", "params": {}}
    )
    assert response.status_code == 404


def test_execute_rejects_operation_from_another_group() -> None:
    operation_id = next(oid for oid in _operation_ids("search") if "search_pt" in oid)
    response = client.post(
        "/web/execute",
        json={"operation_id": operation_id, "group": "pt", "params": {"keyword": "x"}},
    )
    assert response.status_code == 404


def test_execute_requires_path_parameters() -> None:
    operation_id = next(oid for oid in _operation_ids("search") if "search_pt" in oid)
    response = client.post(
        "/web/execute", json={"operation_id": operation_id, "group": "search", "params": {}}
    )
    assert response.status_code == 422


def test_execute_passes_through_binary_responses() -> None:
    operation_id = next(oid for oid in _operation_ids("pt") if "pt_logo" in oid)

    with patch("app.api.common.api_client._make_request") as mock:
        mock.return_value = b"\x89PNG\r\n\x1a\n"
        response = client.post(
            "/web/execute",
            json={"operation_id": operation_id, "group": "pt", "params": {"id_pt": "abc=="}},
        )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content.startswith(b"\x89PNG")


def test_retired_stats_endpoints_are_gone() -> None:
    for path in [
        "/api/stats/mhs-count-gender/",
        "/api/stats/dosen-count-bidang/",
        "/api/stats/pt-count-province/",
        "/api/stats/prodi-count-akreditasi/",
        "/api/stats/mhs-count/",
        "/api/stats/dosen-count/",
    ]:
        assert client.get(path).status_code == 404, path


def test_surviving_stats_endpoints_are_routed(upstream) -> None:
    upstream.return_value = {"status": "success", "data": {"jumlah": 4416}}
    for path in [
        "/api/stats/pt-count/",
        "/api/stats/prodi-count/",
        "/api/stats/mhs-count-active/",
        "/api/stats/dosen-count-active/",
        "/api/stats/prodi-count-bidang-ilmu-terbanyak/",
    ]:
        assert client.get(path).status_code == 200, path


def test_overview_reports_upstream_configuration() -> None:
    payload: dict[str, Any] = client.get("/api/").json()
    assert payload["upstream"]["primary"]["configured"] is True
    assert payload["upstream"]["primary"]["requires_credentials"] is False
