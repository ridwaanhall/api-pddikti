from typing import Any
from urllib.parse import quote, unquote
import ipaddress
import threading
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.core.config import get_settings
from app.core.request_context import get_request_client_ip


# Optional TLS-fingerprint impersonation. Header spoofing alone does not get past an edge
# that fingerprints the TLS handshake (JA3) -- which is what rejects datacenter egress
# while the same headers succeed from a residential connection. When curl_cffi is
# installed the client performs a real Chrome handshake; otherwise it falls back to
# requests, which still works wherever the IP itself is not the problem.
try:  # pragma: no cover - import guard depends on the deployment image
    from curl_cffi import requests as curl_requests
except ImportError:  # pragma: no cover
    curl_requests = None


def _transport_error_types() -> tuple[type[BaseException], ...]:
    """Exception classes both transports can raise, resolved defensively.

    curl_cffi has moved its error class between `errors` and `exceptions` across
    versions, so look in both rather than pinning to one layout.
    """
    types: tuple[type[BaseException], ...] = (requests.exceptions.RequestException,)
    if curl_requests is not None:
        for module_name in ("errors", "exceptions"):
            module = getattr(curl_requests, module_name, None)
            candidate = getattr(module, "RequestsError", None) if module else None
            if isinstance(candidate, type) and issubclass(candidate, BaseException):
                types += (candidate,)
    return types


TRANSPORT_ERRORS = _transport_error_types()


# One coherent browser identity, mirroring a real session against the upstream site. The
# User-Agent, the sec-ch-ua hints and the TLS profile all describe the same browser
# build; a mismatch between any of them is itself a bot signal.
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"
)
CLIENT_HINT_HEADERS = {
    "sec-ch-ua": '"Not=A?Brand";v="99", "Microsoft Edge";v="151", "Chromium";v="151"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"151.0.4129.107"',
    "sec-ch-ua-full-version-list": (
        '"Not=A?Brand";v="99.0.0.0", "Microsoft Edge";v="151.0.4129.107", '
        '"Chromium";v="151.0.7922.174"'
    ),
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"19.0.0"',
}


def _is_public_ip(value: str | None) -> bool:
    """True when the address is routable on the public internet."""
    if not value:
        return False
    try:
        address = ipaddress.ip_address(value.strip().strip("[]"))
    except ValueError:
        return False
    return not (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    )


def _classify_error(exc: BaseException) -> str:
    """Normalize a transport failure into one of our reason strings."""
    if isinstance(exc, requests.exceptions.Timeout):
        return "timeout"
    if isinstance(exc, requests.exceptions.ConnectionError):
        return "connection error"
    if isinstance(exc, requests.exceptions.RequestException):
        return "request error"
    # curl_cffi surfaces everything as one class; fall back to the message.
    message = str(exc).lower()
    if "timed out" in message or "timeout" in message:
        return "timeout"
    return "connection error"


class _PublicIPCache:
    """Caches this server's own public IP so the lookup is not repeated per request."""

    def __init__(self) -> None:
        self._value: str | None = None
        self._expires_at = 0.0
        self._lock = threading.Lock()

    def get(self, session: Any, url: str, timeout: int, ttl: int) -> str | None:
        # Guard on the deadline, not on _value: a failed lookup must back off too.
        if time.monotonic() < self._expires_at:
            return self._value

        with self._lock:
            # Another thread may have refreshed while this one waited.
            if time.monotonic() < self._expires_at:
                return self._value
            try:
                response = session.get(
                    url,
                    timeout=timeout,
                    headers={
                        "accept": "application/json",
                        "user-agent": BROWSER_USER_AGENT,
                    },
                )
                resolved = response.json().get("ip")
            except (*TRANSPORT_ERRORS, ValueError, AttributeError):
                resolved = None

            if _is_public_ip(resolved):
                self._value = resolved
                self._expires_at = time.monotonic() + ttl
            else:
                # Back off briefly so a failing lookup does not stall every request.
                self._expires_at = time.monotonic() + 60
            return self._value

    def clear(self) -> None:
        self._value = None
        self._expires_at = 0.0


class APIClient:
    """HTTP client for forwarding requests to the configured upstream.

    Requests go to the primary upstream first. That surface needs no credentials but
    returns some payloads encrypted, in which case the ciphertext is transparently
    exchanged for plaintext via the upstream's own decrypt endpoint before the caller
    ever sees it. An authenticated upstream can be configured as a fallback for when the
    primary host is unreachable.

    Every host involved comes from the environment; none is hardcoded here.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.public_base = settings.upstream_base_url.rstrip("/")
        self.fallback_base = settings.ridwaanhall_main_api.rstrip("/")
        self.site_origin = settings.upstream_origin.rstrip("/")
        self.decrypt_url = settings.upstream_decrypt_url
        self.timeout = settings.api_timeout
        self.decrypt_timeout = settings.decrypt_timeout

        # Only populated when an authenticated upstream is actually configured.
        self.fallback_headers: dict[str, str] = {}
        if self.fallback_base:
            self.fallback_headers = {
                key: value
                for key, value in (
                    (settings.ridwaanhall_api_x, settings.ridwaanhall_api_key),
                    (settings.ridwaanhall_x, settings.ridwaanhall_key),
                    (settings.ridwaanhall_hash_x, settings.ridwaanhall_hash_key),
                )
                if key
            }

        self.session, self.transport_name = self._build_session()
        self.accept_encoding = self._supported_accept_encoding()
        self._public_ip = _PublicIPCache()

    def _build_session(self) -> tuple[Any, str]:
        impersonate = self.settings.upstream_impersonate
        if curl_requests is not None and impersonate:
            return (
                curl_requests.Session(impersonate=impersonate),
                f"curl_cffi:{impersonate}",
            )

        session = requests.Session()
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=Retry(
                total=2,
                connect=2,
                read=1,
                backoff_factor=0.4,
                status_forcelist=(),
                allowed_methods=frozenset({"GET", "POST"}),
            ),
        )
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session, "requests"

    def _supported_accept_encoding(self) -> str:
        """Advertise only what this transport can actually decode.

        Claiming br/zstd without a decoder available would hand us undecodable
        response bodies, so the header tracks real capability rather than copying
        the browser blindly.
        """
        if self.transport_name.startswith("curl_cffi"):
            return "gzip, deflate, br, zstd"

        codings = ["gzip", "deflate"]
        for module_name, coding in (("brotli", "br"), ("brotlicffi", "br"), ("zstandard", "zstd")):
            if coding in codings:
                continue
            try:
                __import__(module_name)
            except ImportError:
                continue
            codings.append(coding)
        return ", ".join(codings)

    # ------------------------------------------------------------------ headers

    def _client_ip(self) -> str | None:
        """Resolve the IP to advertise upstream.

        Prefers the IP of whoever called this API, so the upstream sees the end user's
        location rather than the hosting platform's egress. Falls back to this server's
        own public address only when the caller's IP is missing or not routable (local
        development, internal health checks).
        """
        caller_ip = get_request_client_ip()
        if _is_public_ip(caller_ip):
            return caller_ip
        if not self.settings.ip_lookup_url:
            return None
        return self._public_ip.get(
            self.session,
            self.settings.ip_lookup_url,
            self.timeout,
            self.settings.ip_cache_ttl,
        )

    def _browser_headers(self, referer: str | None = None) -> dict[str, str]:
        """The exact header set a browser sends to the upstream site.

        Deliberately does NOT include X-Forwarded-For or X-Real-IP: no browser sends
        those, and a client-supplied forwarding header reads as proxy spoofing to a
        protective edge. The upstream's own `x-user-ip` carries the caller IP instead.
        """
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": self.accept_encoding,
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "dnt": "1",
            "priority": "u=1, i",
            "referer": referer or f"{self.site_origin}/",
            **CLIENT_HINT_HEADERS,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": BROWSER_USER_AGENT,
        }
        if self.settings.upstream_cookie:
            headers["cookie"] = self.settings.upstream_cookie
        return headers

    # ------------------------------------------------------------------ decrypt

    @staticmethod
    def _is_encrypted_envelope(payload: Any) -> bool:
        return (
            isinstance(payload, dict)
            and payload.get("status") == "success"
            and isinstance(payload.get("data"), str)
            and len(payload["data"]) > 32
        )

    def _decrypt(self, ciphertext: str, referer: str | None = None) -> Any:
        """Exchange an encrypted payload for plaintext JSON via the decrypt endpoint."""
        if not self.decrypt_url:
            raise RuntimeError("no decrypt endpoint configured")

        # Matches the browser exactly: */* accept, text/plain body, origin set, and no
        # x-user-ip (the site does not send it on this call).
        headers = self._browser_headers(referer)
        headers["accept"] = "*/*"
        headers["content-type"] = "text/plain"
        headers["origin"] = self.site_origin

        reasons: list[str] = []
        for _ in range(2):
            try:
                response = self.session.post(
                    self.decrypt_url,
                    data=ciphertext.encode("utf-8"),
                    headers=headers,
                    timeout=self.decrypt_timeout,
                )
            except TRANSPORT_ERRORS as exc:
                reasons.append(_classify_error(exc))
                continue

            if response.status_code < 400:
                try:
                    return response.json()
                except ValueError:
                    reasons.append("invalid json")
                    continue
            reasons.append(f"http {response.status_code}")

        # Carry the reason out: a generic "decryption failed" hides whether this was a
        # block, a timeout, or a misconfiguration.
        raise RuntimeError("; ".join(reasons) or "unknown error")

    # ------------------------------------------------------------------ responses

    def _handle_response(self, response: Any, referer: str | None = None) -> Any:
        content_type = response.headers.get("Content-Type", "")

        if "image" in content_type:
            return response.content

        try:
            payload = response.json()
        except ValueError:
            return {
                "code": 502,
                "error": "Invalid JSON response",
                "message": "The external API returned malformed JSON.",
            }

        if not self._is_encrypted_envelope(payload):
            return payload

        # Second leg of the two-step flow: the first response carried ciphertext.
        try:
            decrypted = self._decrypt(payload["data"], referer)
        except RuntimeError as exc:
            return {
                "code": 502,
                "error": "Decryption failed",
                "message": (
                    "The external API returned an encrypted payload that could not be "
                    "decrypted. Please try again later."
                ),
                "decrypt_failure": str(exc),
                "transport": self.transport_name,
            }
        # Re-wrap so encrypted and plain endpoints share one response shape.
        return {"status": "success", "data": decrypted}

    # ------------------------------------------------------------------ requests

    def _attempts(
        self, referer: str | None = None
    ) -> list[tuple[str, str, dict[str, str]]]:
        attempts: list[tuple[str, str, dict[str, str]]] = []

        if self.public_base:
            headers = self._browser_headers(referer)
            client_ip = self._client_ip()
            if client_ip:
                headers["x-user-ip"] = client_ip
            attempts.append(("public", self.public_base, headers))

        if self.fallback_base:
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9,id;q=0.8",
                "user-agent": BROWSER_USER_AGENT,
                **self.fallback_headers,
            }
            attempts.append(("authenticated", self.fallback_base, headers))

        return attempts

    def _make_request(
        self,
        endpoint: str,
        params: dict[str, str] | None = None,
        referer: str | None = None,
    ) -> Any:
        attempts = self._attempts(referer)
        if not attempts:
            return {
                "code": 503,
                "error": "No upstream configured",
                "message": (
                    "No upstream base URL is configured. Set UPSTREAM_BASE_URL or "
                    "RIDWAANHALL_MAIN_API in the deployment environment."
                ),
            }

        path = endpoint.lstrip("/")
        failures: list[dict[str, str]] = []
        timed_out = False

        for name, base, headers in attempts:
            try:
                response = self.session.get(
                    f"{base}/{path}",
                    headers=headers,
                    timeout=self.timeout,
                    params=params,
                )
            except TRANSPORT_ERRORS as exc:
                reason = _classify_error(exc)
                timed_out = timed_out or reason == "timeout"
                failures.append({"upstream": name, "reason": reason})
                continue

            # A block or an upstream fault is worth retrying on the other base; any other
            # status is a real answer and belongs to the caller.
            if response.status_code == 403 or response.status_code >= 500:
                failures.append(
                    {"upstream": name, "reason": f"http {response.status_code}"}
                )
                continue

            if response.status_code < 400:
                return self._handle_response(response, referer)

            try:
                message = response.json()
            except ValueError:
                message = response.text
            return {
                "code": response.status_code,
                "error": "HTTP error occurred",
                "message": message,
            }

        if timed_out:
            return {
                "code": 408,
                "error": "Request timed out",
                "message": (
                    "External API request timed out after "
                    f"{self.timeout} seconds. Please try again later."
                ),
                "timeout_seconds": self.timeout,
                "upstreams_tried": failures,
                "transport": self.transport_name,
            }

        return {
            "code": 503,
            "error": "Connection error",
            "message": "Unable to connect to the external API. Please try again later.",
            "upstreams_tried": failures,
            "transport": self.transport_name,
        }

    # ------------------------------------------------------------------ public API

    def get(self, endpoint: str, **kwargs: str) -> Any:
        params = {key: value for key, value in kwargs.items()} if kwargs else None
        return self._make_request(endpoint, params=params)

    @staticmethod
    def _quote_segment(value: str) -> str:
        # '=' must survive: upstream entity IDs are URL-safe base64 and reject %3D
        # padding with "invalid id". Spaces and other unsafe characters are still encoded.
        return quote(unquote(value), safe="=")

    def _search_referer(self, endpoint: str, encoded_value: str) -> str | None:
        """Mirror the referer a browser would carry into this call."""
        if not self.site_origin:
            return None
        if endpoint.startswith("pencarian"):
            return f"{self.site_origin}/search/{encoded_value}"
        return f"{self.site_origin}/"

    def get_with_keyword(self, endpoint: str, keyword: str) -> Any:
        encoded = self._quote_segment(keyword)
        return self._make_request(
            f"{endpoint}/{encoded}", referer=self._search_referer(endpoint, encoded)
        )

    def get_with_id_and_semester(self, endpoint: str, item_id: str, id_thsmt: str) -> Any:
        encoded_id = self._quote_segment(item_id)
        encoded_semester = self._quote_segment(id_thsmt)
        return self._make_request(f"{endpoint}/{encoded_id}/{encoded_semester}")

    def get_with_id_and_param_semester(
        self, endpoint: str, item_id: str, id_thsmt: str
    ) -> Any:
        encoded_id = self._quote_segment(item_id)
        return self._make_request(
            f"{endpoint}/{encoded_id}", params={"semester": id_thsmt}
        )
