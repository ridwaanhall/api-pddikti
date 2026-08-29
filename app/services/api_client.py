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


# One coherent browser identity. Cloudflare in front of PDDikti rejects unknown clients
# outright (a default python UA gets a hard 403), and a User-Agent that disagrees with the
# sec-ch-ua client hints is itself a bot signal -- so these values must be kept in sync.
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"
)
SEC_CH_UA = '"Not=A?Brand";v="99", "Microsoft Edge";v="151", "Chromium";v="151"'
SEC_CH_UA_PLATFORM = '"Windows"'


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


class _PublicIPCache:
    """Caches this server's own public IP so ipify is not called per request."""

    def __init__(self) -> None:
        self._value: str | None = None
        self._expires_at = 0.0
        self._lock = threading.Lock()

    def get(self, session: requests.Session, url: str, timeout: int, ttl: int) -> str | None:
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
            except (requests.exceptions.RequestException, ValueError, AttributeError):
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
    """HTTP client for forwarding requests to the upstream PDDikti API.

    Requests go to the public PDDikti web API first. That surface needs no credentials but
    returns some payloads encrypted, in which case the ciphertext is transparently exchanged
    for plaintext via the site's own decrypt endpoint before the caller ever sees it. An
    authenticated upstream can be configured as a fallback for when the public host is
    unreachable.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.public_base = settings.pddikti_public_base.rstrip("/")
        self.fallback_base = settings.ridwaanhall_main_api.rstrip("/")
        self.site_origin = settings.pddikti_site_origin.rstrip("/")
        self.decrypt_url = settings.pddikti_decrypt_url
        self.timeout = settings.api_timeout

        # Only populated when an authenticated upstream is actually configured.
        self.fallback_headers: dict[str, str] = {}
        if self.fallback_base:
            self.fallback_headers = {
                settings.ridwaanhall_api_x: settings.ridwaanhall_api_key,
                settings.ridwaanhall_x: settings.ridwaanhall_key,
                settings.ridwaanhall_hash_x: settings.ridwaanhall_hash_key,
            }

        self.session = requests.Session()
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
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self._public_ip = _PublicIPCache()

    # ------------------------------------------------------------------ headers

    def _client_ip(self) -> str | None:
        """Resolve the IP to advertise upstream.

        Prefers the IP of whoever called this API, so PDDikti sees the end user's location
        rather than the hosting platform's egress. Falls back to this server's own public
        address only when the caller's IP is missing or not routable (local development,
        internal health checks).
        """
        caller_ip = get_request_client_ip()
        if _is_public_ip(caller_ip):
            return caller_ip
        return self._public_ip.get(
            self.session,
            self.settings.ipify_url,
            self.timeout,
            self.settings.ip_cache_ttl,
        )

    def _browser_headers(self) -> dict[str, str]:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "dnt": "1",
            "priority": "u=1, i",
            "referer": f"{self.site_origin}/",
            "sec-ch-ua": SEC_CH_UA,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": SEC_CH_UA_PLATFORM,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": BROWSER_USER_AGENT,
        }
        client_ip = self._client_ip()
        if client_ip:
            headers["x-user-ip"] = client_ip
            headers["X-Forwarded-For"] = client_ip
            headers["X-Real-IP"] = client_ip
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

    def _decrypt(self, ciphertext: str) -> Any:
        """Exchange an encrypted payload for plaintext JSON via the site's decrypt endpoint."""
        headers = self._browser_headers()
        headers["accept"] = "*/*"
        headers["content-type"] = "text/plain"
        headers["origin"] = self.site_origin

        last_error: Exception | None = None
        for _ in range(2):
            try:
                response = self.session.post(
                    self.decrypt_url,
                    data=ciphertext.encode("utf-8"),
                    headers=headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
            except (requests.exceptions.RequestException, ValueError) as exc:
                last_error = exc
        raise RuntimeError("decrypt step failed") from last_error

    # ------------------------------------------------------------------ responses

    def _handle_response(self, response: requests.Response) -> Any:
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
            decrypted = self._decrypt(payload["data"])
        except RuntimeError:
            return {
                "code": 502,
                "error": "Decryption failed",
                "message": (
                    "The external API returned an encrypted payload that could not be "
                    "decrypted. Please try again later."
                ),
            }
        # Re-wrap so encrypted and plain endpoints share one response shape.
        return {"status": "success", "data": decrypted}

    # ------------------------------------------------------------------ requests

    def _attempts(self) -> list[tuple[str, str, dict[str, str]]]:
        attempts: list[tuple[str, str, dict[str, str]]] = []
        if self.public_base:
            attempts.append(("public", self.public_base, self._browser_headers()))
        if self.fallback_base:
            headers = {
                "accept": "application/json, text/plain, */*",
                "user-agent": BROWSER_USER_AGENT,
                **self.fallback_headers,
            }
            attempts.append(("authenticated", self.fallback_base, headers))
        return attempts

    def _make_request(self, endpoint: str, params: dict[str, str] | None = None) -> Any:
        attempts = self._attempts()
        if not attempts:
            return {
                "code": 503,
                "error": "No upstream configured",
                "message": (
                    "No upstream base URL is configured. Set PDDIKTI_PUBLIC_BASE or "
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
            except requests.exceptions.Timeout:
                timed_out = True
                failures.append({"upstream": name, "reason": "timeout"})
                continue
            except requests.exceptions.ConnectionError:
                failures.append({"upstream": name, "reason": "connection error"})
                continue
            except requests.exceptions.RequestException:
                failures.append({"upstream": name, "reason": "request error"})
                continue

            # A block or an upstream fault is worth retrying on the other base; any other
            # status is a real answer and belongs to the caller.
            if response.status_code == 403 or response.status_code >= 500:
                failures.append({"upstream": name, "reason": f"http {response.status_code}"})
                continue

            if response.ok:
                return self._handle_response(response)

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
            }

        return {
            "code": 503,
            "error": "Connection error",
            "message": "Unable to connect to the external API. Please try again later.",
            "upstreams_tried": failures,
        }

    # ------------------------------------------------------------------ public API

    def get(self, endpoint: str, **kwargs: str) -> Any:
        params = {key: value for key, value in kwargs.items()} if kwargs else None
        return self._make_request(endpoint, params=params)

    @staticmethod
    def _quote_segment(value: str) -> str:
        # '=' must survive: PDDikti entity IDs are URL-safe base64 and reject %3D padding
        # with "invalid id". Spaces and other unsafe characters are still encoded.
        return quote(unquote(value), safe="=")

    def get_with_keyword(self, endpoint: str, keyword: str) -> Any:
        return self._make_request(f"{endpoint}/{self._quote_segment(keyword)}")

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
