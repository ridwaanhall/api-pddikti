"""Unit tests for the upstream client: the two-step decrypt flow, IP forwarding,
segment encoding, and the public/authenticated fallback chain.

Everything here is offline -- requests is stubbed so no test touches the network.
"""

from typing import Any
import json

import pytest
import requests

from app.core import request_context
from app.services import api_client as api_client_module
from app.services.api_client import APIClient, _is_public_ip


class FakeResponse:
    def __init__(
        self,
        payload: Any = None,
        status_code: int = 200,
        content_type: str = "application/json",
        content: bytes | None = None,
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.headers = {"Content-Type": content_type}
        self.content = content if content is not None else b""
        self.text = "" if payload is None else json.dumps(payload)

    @property
    def ok(self) -> bool:
        return self.status_code < 400

    def json(self) -> Any:
        if self._payload is None:
            raise ValueError("no json")
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(response=self)


class FakeSession:
    """Records calls and replays queued outcomes; an Exception in the queue is raised."""

    def __init__(self) -> None:
        self.get_calls: list[dict[str, Any]] = []
        self.post_calls: list[dict[str, Any]] = []
        self.get_results: list[Any] = []
        self.post_results: list[Any] = []

    def mount(self, *_args, **_kwargs) -> None:  # pragma: no cover - adapter setup
        pass

    def get(self, url, headers=None, timeout=None, params=None):
        self.get_calls.append({"url": url, "headers": headers or {}, "params": params})
        result = self.get_results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    def post(self, url, data=None, headers=None, timeout=None):
        self.post_calls.append({"url": url, "data": data, "headers": headers or {}})
        result = self.post_results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


@pytest.fixture
def client(monkeypatch) -> APIClient:
    instance = APIClient()
    instance.session = FakeSession()
    instance._public_ip.clear()
    # A public caller IP by default, so the public-IP lookup is not consulted.
    monkeypatch.setattr(
        api_client_module, "get_request_client_ip", lambda: "158.140.170.57"
    )
    return instance


# --------------------------------------------------------------------- encoding


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        # Entity IDs are URL-safe base64: the padding must survive, or upstream
        # answers 400 invalid id.
        ("muM28NSb_I4rz-obNKpgpKA==", "muM28NSb_I4rz-obNKpgpKA=="),
        ("ridwan halim uty", "ridwan%20halim%20uty"),
        ("gadjah mada", "gadjah%20mada"),
    ],
)
def test_quote_segment_preserves_padding_and_encodes_spaces(raw, expected) -> None:
    assert APIClient._quote_segment(raw) == expected


def test_get_with_keyword_builds_path(client) -> None:
    client.session.get_results.append(FakeResponse({"status": "success", "data": []}))
    client.get_with_keyword("pencarian/pt", "gadjah mada")
    assert client.session.get_calls[0]["url"].endswith("/pencarian/pt/gadjah%20mada")


def test_param_semester_is_sent_as_query(client) -> None:
    client.session.get_results.append(FakeResponse({"status": "success", "data": []}))
    client.get_with_id_and_param_semester("dosen/homebase", "abc==", "20241")

    call = client.session.get_calls[0]
    assert call["url"].endswith("/dosen/homebase/abc==")
    assert call["params"] == {"semester": "20241"}


# ---------------------------------------------------------------- decrypt flow


def test_encrypted_envelope_is_decrypted_and_rewrapped(client) -> None:
    ciphertext = "9lqDIEAB" + "x" * 90
    client.session.get_results.append(
        FakeResponse({"status": "success", "data": ciphertext})
    )
    client.session.post_results.append(
        FakeResponse({"mahasiswa": [{"nama": "RIDWAN HALIM"}]})
    )

    result = client.get_with_keyword("pencarian/enc/all", "ridwan halim")

    # The ciphertext was posted verbatim as text/plain to the decrypt endpoint.
    post = client.session.post_calls[0]
    assert post["url"] == client.decrypt_url
    assert post["data"] == ciphertext.encode("utf-8")
    assert post["headers"]["content-type"] == "text/plain"

    # Shape matches the plain endpoints so callers see one envelope.
    assert result == {
        "status": "success",
        "data": {"mahasiswa": [{"nama": "RIDWAN HALIM"}]},
    }


def test_plain_payload_is_passed_through_untouched(client) -> None:
    payload = {"status": "success", "data": [{"id": "abc", "nama": "UGM"}]}
    client.session.get_results.append(FakeResponse(payload))

    assert client.get("pencarian/pt/mada") == payload
    assert client.session.post_calls == []  # no decrypt leg


def test_short_string_data_is_not_treated_as_ciphertext(client) -> None:
    payload = {"status": "success", "data": "OK"}
    client.session.get_results.append(FakeResponse(payload))

    assert client.get("some/endpoint") == payload
    assert client.session.post_calls == []


def test_decrypt_failure_reports_502(client) -> None:
    client.session.get_results.append(
        FakeResponse({"status": "success", "data": "9lqDIEAB" + "x" * 90})
    )
    client.session.post_results.extend(
        [requests.exceptions.ConnectionError(), requests.exceptions.ConnectionError()]
    )

    result = client.get("pencarian/enc/all/x")
    assert result["code"] == 502
    assert result["error"] == "Decryption failed"


def test_image_response_returns_raw_bytes(client) -> None:
    client.session.get_results.append(
        FakeResponse(content_type="image/png", content=b"\x89PNG")
    )
    assert client.get_with_keyword("pt/logo", "abc==") == b"\x89PNG"


# ------------------------------------------------------------------ client IP


def test_caller_ip_is_forwarded_upstream(client) -> None:
    client.session.get_results.append(FakeResponse({"status": "success", "data": []}))
    client.get("pt/count")

    headers = client.session.get_calls[0]["headers"]
    assert headers["x-user-ip"] == "158.140.170.57"
    assert headers["X-Forwarded-For"] == "158.140.170.57"
    assert "Chrome" in headers["user-agent"]


def test_private_caller_ip_falls_back_to_public_lookup(client, monkeypatch) -> None:
    monkeypatch.setattr(api_client_module, "get_request_client_ip", lambda: "127.0.0.1")
    # First GET answers the public-IP lookup, second is the real upstream call.
    client.session.get_results.append(FakeResponse({"ip": "45.64.99.10"}))
    client.session.get_results.append(FakeResponse({"status": "success", "data": []}))

    client.get("pt/count")

    assert client.session.get_calls[0]["url"] == client.settings.ip_lookup_url
    assert client.session.get_calls[1]["headers"]["x-user-ip"] == "45.64.99.10"


def test_public_ip_lookup_is_cached_across_requests(client, monkeypatch) -> None:
    monkeypatch.setattr(api_client_module, "get_request_client_ip", lambda: None)
    client.session.get_results.append(FakeResponse({"ip": "45.64.99.10"}))
    client.session.get_results.append(FakeResponse({"status": "success", "data": []}))
    client.session.get_results.append(FakeResponse({"status": "success", "data": []}))

    client.get("pt/count")
    client.get("prodi/count")

    lookup_calls = [
        call for call in client.session.get_calls if call["url"] == client.settings.ip_lookup_url
    ]
    assert len(lookup_calls) == 1


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("158.140.170.57", True),
        ("2404:6800:4003::1", True),
        ("127.0.0.1", False),
        ("10.0.0.4", False),
        ("192.168.1.1", False),
        ("169.254.1.1", False),
        ("not-an-ip", False),
        (None, False),
    ],
)
def test_is_public_ip(value, expected) -> None:
    assert _is_public_ip(value) is expected


def test_request_context_ip_reaches_headers(client, monkeypatch) -> None:
    monkeypatch.setattr(
        api_client_module, "get_request_client_ip", request_context.get_request_client_ip
    )
    tokens = request_context.set_request_identity("8.8.4.4", "pytest")
    try:
        client.session.get_results.append(FakeResponse({"status": "success", "data": []}))
        client.get("pt/count")
    finally:
        request_context.reset_request_identity(tokens)

    assert client.session.get_calls[0]["headers"]["x-user-ip"] == "8.8.4.4"


# ------------------------------------------------------------- fallback chain


def test_connection_error_falls_back_to_authenticated_upstream(client) -> None:
    client.fallback_base = "https://authed.example"
    client.fallback_headers = {"Host": "authed.example"}

    client.session.get_results.append(requests.exceptions.ConnectionError())
    client.session.get_results.append(
        FakeResponse({"status": "success", "data": {"jumlah": 1}})
    )

    result = client.get("pt/count")

    assert result == {"status": "success", "data": {"jumlah": 1}}
    assert client.session.get_calls[1]["url"].startswith("https://authed.example/")
    assert client.session.get_calls[1]["headers"]["Host"] == "authed.example"


def test_403_falls_back_then_reports_which_upstreams_failed(client) -> None:
    client.fallback_base = "https://authed.example"
    client.fallback_headers = {}

    client.session.get_results.append(FakeResponse(status_code=403))
    client.session.get_results.append(requests.exceptions.ConnectionError())

    result = client.get("pt/count")

    assert result["code"] == 503
    assert result["error"] == "Connection error"
    assert result["upstreams_tried"] == [
        {"upstream": "public", "reason": "http 403"},
        {"upstream": "authenticated", "reason": "connection error"},
    ]


def test_client_error_is_returned_without_falling_back(client) -> None:
    client.fallback_base = "https://authed.example"
    client.session.get_results.append(
        FakeResponse({"message": "invalid id"}, status_code=400)
    )

    result = client.get("pt/detail/x")

    assert result["code"] == 400
    # A 4xx is a real answer from upstream, not a signal to try the other base.
    assert len(client.session.get_calls) == 1


def test_timeout_reports_408(client) -> None:
    client.fallback_base = ""
    client.session.get_results.append(requests.exceptions.Timeout())

    result = client.get("pt/count")
    assert result["code"] == 408
    assert result["timeout_seconds"] == client.timeout


def test_no_upstream_configured_is_distinguishable(client) -> None:
    client.public_base = ""
    client.fallback_base = ""

    result = client.get("pt/count")
    assert result["code"] == 503
    assert result["error"] == "No upstream configured"
