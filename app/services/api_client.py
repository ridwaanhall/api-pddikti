from typing import Any
from urllib.parse import quote, unquote
import random

import requests

from app.core.config import get_settings
from app.core.request_context import get_request_client_ip, get_request_user_agent


RANDOM_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Mobile/15E148 Safari/604.1",
]


class APIClient:
    """HTTP client for forwarding requests to the upstream PDDikti API."""

    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.ridwaanhall_main_api.rstrip("/")
        self.headers = {
            settings.ridwaanhall_api_x: settings.ridwaanhall_api_key,
            settings.ridwaanhall_x: settings.ridwaanhall_key,
            settings.ridwaanhall_hash_x: settings.ridwaanhall_hash_key,
        }
        self.timeout = settings.api_timeout

    def _handle_response(self, response: requests.Response) -> Any:
        content_type = response.headers.get("Content-Type", "")

        if response.ok:
            if "image" in content_type:
                return response.content
            try:
                return response.json()
            except ValueError:
                return {
                    "code": 502,
                    "error": "Invalid JSON response",
                    "message": "The external API returned malformed JSON.",
                }

        try:
            message = response.json()
        except ValueError:
            message = response.text

        return {
            "code": response.status_code,
            "error": "HTTP error occurred",
            "message": message,
        }

    def _make_request(self, url: str, params: dict[str, str] | None = None) -> Any:
        try:
            request_headers = dict(self.headers)
            client_ip = get_request_client_ip()
            if client_ip:
                request_headers["X-Forwarded-For"] = client_ip
                request_headers["X-Real-IP"] = client_ip

            incoming_user_agent = get_request_user_agent()
            if incoming_user_agent:
                request_headers["X-Original-User-Agent"] = incoming_user_agent

            request_headers["User-Agent"] = random.choice(RANDOM_USER_AGENTS)

            response = requests.get(
                url,
                headers=request_headers,
                timeout=self.timeout,
                params=params,
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            return {
                "code": 408,
                "error": "Request timed out",
                "message": (
                    "External API request timed out after "
                    f"{self.timeout} seconds. Please try again later."
                ),
                "timeout_seconds": self.timeout,
            }
        except requests.exceptions.ConnectionError:
            return {
                "code": 503,
                "error": "Connection error",
                "message": "Unable to connect to the external API. Please try again later.",
            }
        except requests.exceptions.RequestException:
            return {
                "code": 500,
                "error": "An unexpected error occurred",
                "message": "Please try again later or contact the administrator.",
            }

    def get(self, endpoint: str, **kwargs: str) -> Any:
        url = f"{self.base_url}/{endpoint}"
        params = {key: value for key, value in kwargs.items()} if kwargs else None
        return self._make_request(url, params=params)

    @staticmethod
    def _quote_segment(value: str) -> str:
        return quote(unquote(value), safe="")

    def get_with_keyword(self, endpoint: str, keyword: str) -> Any:
        encoded_keyword = self._quote_segment(keyword)
        url = f"{self.base_url}/{endpoint}/{encoded_keyword}"
        return self._make_request(url)

    def get_with_id_and_semester(self, endpoint: str, item_id: str, id_thsmt: str) -> Any:
        encoded_id = self._quote_segment(item_id)
        encoded_semester = self._quote_segment(id_thsmt)
        url = f"{self.base_url}/{endpoint}/{encoded_id}/{encoded_semester}"
        return self._make_request(url)

    def get_with_id_and_param_semester(
        self, endpoint: str, item_id: str, id_thsmt: str
    ) -> Any:
        encoded_id = self._quote_segment(item_id)
        url = f"{self.base_url}/{endpoint}/{encoded_id}"
        return self._make_request(url, params={"semester": id_thsmt})
