# DEPRECATED: Most endpoints have been removed and this API is no longer supported.

import json
from typing import Any, Dict, Optional, Union
from urllib.parse import unquote

import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

BASE_URL = settings.RIDWAANHALL_MAIN_API


class APIClient:
    """
    A class to handle making requests to the RIDWAANHALL API.
    """

    def __init__(self):
        self.headers = {
            settings.RIDWAANHALL_API_X: settings.RIDWAANHALL_API_KEY,
            settings.RIDWAANHALL_X: settings.RIDWAANHALL_KEY,
            settings.RIDWAANHALL_HASH_X: settings.RIDWAANHALL_HASH_KEY,
        }
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handles the response from the API.

        Args:
            response (requests.Response): The response object from the API.

        Returns:
             Any: The JSON response data or None for images.
        """
        try:
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            if "image" in response.headers.get("Content-Type", ""):
                return response.content  # Return raw content for images
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {
                "code": response.status_code,
                "error": "HTTP error occurred",
                "message": response.json(),
            }
        except requests.exceptions.ConnectionError as conn_err:
            return {
                "code": response.status_code,
                "error": "Connection error occurred",
                "message": response.json(),
            }
        except requests.exceptions.Timeout as timeout_err:
            return {
                "code": response.status_code,
                "error": "Request timed out",
                "message": response.json(),
            }
        except requests.exceptions.RequestException as req_err:
            return {
                "code": response.status_code,
                "error": "An error occurred",
                "message": response.json(),
            }

    def _make_request(self, url: str) -> Any:
        """
        Makes an API request with error handling

        Args:
            url (str): The complete URL for the request.

        Returns:
            Any: The data received from the API or error object.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(url)
            print(self.headers)

            return {
                "error": "An unexpected error occurred", 
                "message": "Please try again later or contact the administrator.",
            }

    def get(self, endpoint: str, **kwargs: str) -> Any:
        """
        Makes a GET request to the RIDWAANHALL API.

        Args:
            endpoint (str): The API endpoint.
            **kwargs (str): Optional parameters for the URL.

        Returns:
           Any: The API response data or None if there was an error.
        """
        url = f"{BASE_URL}/{endpoint}"
        if kwargs:
            params = "&".join([f"{k}={unquote(v)}" for k, v in kwargs.items()])
            url = f"{url}?{params}"

        return self._make_request(url)

    def get_with_keyword(self, endpoint: str, keyword: str) -> Any:
        """
        Makes a GET request with a keyword in the URL.

        Args:
            endpoint (str): The API endpoint.
            keyword (str): The keyword for the request.

        Returns:
             Any: The API response data or None if there was an error.
        """
        decoded_keyword = unquote(keyword)
        url = f"{BASE_URL}/{endpoint}/{decoded_keyword}"
        return self._make_request(url)

    def get_with_id_and_semester(self, endpoint: str, id: str, id_thsmt: str) -> Any:
        """
        Makes a GET request with ID and semester parameters

        Args:
             endpoint (str): The API endpoint.
             id (str): The ID for the request.
             id_thsmt (str): The semester ID.

        Returns:
            Any: The API response data or None if there was an error.
        """
        decoded_keyword = unquote(id)
        url = f"{BASE_URL}/{endpoint}/{decoded_keyword}/{id_thsmt}"
        return self._make_request(url)

    def get_with_id_and_param_semester(self, endpoint: str, id: str, id_thsmt: str) -> Any:
        """
        Makes a GET request with ID and semester parameters

        Args:
             endpoint (str): The API endpoint.
             id (str): The ID for the request.
             id_thsmt (str): The semester ID.

        Returns:
            Any: The API response data or None if there was an error.
        """
        decoded_keyword = unquote(id)
        url = f"{BASE_URL}/{endpoint}/{decoded_keyword}?semester={id_thsmt}"
        return self._make_request(url)


class BaseAPIView(APIView):
    """
    Base class for API views, providing common functionality.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()

    def handle_api_response(self, data: Any) -> Response:
        """
        Handles the API response and returns a Response object

        Args:
             data (Any): The data received from the API.

        Returns:
            Response: The API response for client
        """
        return Response(data)


# API Views
class APIOverview(BaseAPIView):
    def get(self, _):
        with open("api_overview.json", "r") as file:
            data = json.load(file)
        return self.handle_api_response(data)
