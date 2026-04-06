from typing import Any
from urllib.parse import unquote

import requests

from app.core.config import get_settings


class APIClient:
    """HTTP client for forwarding requests to the upstream PDDIKTI API."""

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

    def _make_request(self, url: str) -> Any:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
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
        if kwargs:
            params = "&".join([f"{k}={unquote(v)}" for k, v in kwargs.items()])
            url = f"{url}?{params}"

        return self._make_request(url)

    def get_with_keyword(self, endpoint: str, keyword: str) -> Any:
        decoded_keyword = unquote(keyword)
        url = f"{self.base_url}/{endpoint}/{decoded_keyword}"
        return self._make_request(url)

    def get_with_id_and_semester(self, endpoint: str, item_id: str, id_thsmt: str) -> Any:
        decoded_id = unquote(item_id)
        url = f"{self.base_url}/{endpoint}/{decoded_id}/{id_thsmt}"
        return self._make_request(url)

    def get_with_id_and_param_semester(
        self, endpoint: str, item_id: str, id_thsmt: str
    ) -> Any:
        decoded_id = unquote(item_id)
        url = f"{self.base_url}/{endpoint}/{decoded_id}?semester={id_thsmt}"
        return self._make_request(url)
