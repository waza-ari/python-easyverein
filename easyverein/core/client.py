"""
Main EasyVerein API class
"""
import logging
from typing import Type, TypeVar

import requests
from pydantic import BaseModel

from .exceptions import EasyvereinAPIException, EasyvereinAPITooManyRetriesException

T = TypeVar("T")


class EasyvereinClient:
    """
    Class encapsulating common function used by all API methods
    """

    def __init__(self, api_key, api_version, base_url, logger: logging.Logger):
        """
        Constructor setting API key and logger
        """
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version
        self.logger = logger

    def _get_header(self):
        """
        Constructs a header for the API request
        """
        return {"Authorization": "Token " + self.api_key}

    def get_url(self, path):
        """
        Constructs a URL for the API request
        """
        return f"{self.base_url}{self.api_version}{path}"

    def _do_request(  # noqa: PLR0913
        self, method, url, data=None, headers=None, files=None
    ):
        """
        Helper method that performs an actual call against the API,
        fetching the most common errors
        """
        self.logger.debug("Performing %s request to %s", method, url)

        # Merge auth header with custom headers
        final_headers = self._get_header() | (headers or {})

        func = getattr(requests, method)
        if data:
            res = func(url, headers=final_headers, json=data, files=files or {})
        else:
            res = func(url, headers=final_headers, files=files)

        self.logger.debug("Request returned status code %d", res.status_code)

        if res.status_code == 429:
            retry_after = res.headers("Retry-After")
            self.logger.warning(
                "Request returned status code 429, too many requests. Wait %d seconds",
                retry_after,
            )
            raise EasyvereinAPITooManyRetriesException(
                retry_after,
                f"Too many requests, please wait {retry_after} seconds and try again.",
            )

        if res.status_code == 404:
            self.logger.warning("Request returned status code 404, resource not found")
            raise EasyvereinAPIException("Requested resource not found")

        try:
            content = res.json()
        except ValueError:
            content = None

        return res.status_code, content

    def create(
        self,
        url,
        data: BaseModel = None,
        return_model: Type[T] = None,
        status_code: int = 201,
    ) -> T:
        """
        Method to create an object in the API
        """
        return self._handle_response(
            self._do_request(
                "post", url, data=data.model_dump(exclude_none=True, exclude_unset=True)
            ),
            return_model,
            status_code,
        )

    def delete(self, url, status_code: int = 204):
        """
        Method to delete an object in the API
        """
        return self._handle_response(
            self._do_request("delete", url), expected_status_code=status_code
        )

    def fetch(self, url, model: Type[T] = None) -> list[T]:
        """
        Helper method that fetches a result from an API call

        Only supports GET endpoints
        """
        res = self._do_request("get", url)
        print(res)
        return self._handle_response(res, model, 200)

    def fetch_paginated(self, url, model: Type[T] = None, limit=100) -> list[T]:
        """
        Helper method that fetches all pages of a paginated API call

        Only supports GET endpoints
        """

        self.logger.debug("Fetching paginated API call %s, limit is %d", url, limit)

        # Add limit parameter to URL
        if "?" not in url:
            url += f"?limit={limit}"
        else:
            url += f"&limit={limit}"

        resources = []
        status_code: int = 0

        while url is not None:
            self.logger.debug("Fetching page of paginated API call %s", url)

            status_code, result = self._do_request("get", url)
            self.logger.debug("Request returned status code %d", status_code)

            if not status_code == 200:
                self.logger.error(
                    "Could not fetch paginated API %s, status code %d", url, status_code
                )
                self.logger.debug("API response: %s", result)
                raise EasyvereinAPIException(
                    f"Could not fetch paginated API {url}, "
                    f"status code {status_code}. API response: {result}"
                )

            resources.extend(result["results"])
            url = result["next"]

        return self._handle_response((status_code, resources), model, 200)

    @staticmethod
    def _handle_response(
        res: tuple[int, list], model: Type[T] = None, expected_status_code=200
    ) -> T | list[T]:
        """
        Helper method that handles API responses
        """
        status_code, data = res
        if status_code != expected_status_code:
            raise EasyvereinAPIException(
                f"API returned status code {status_code}. API response: {data}"
            )

        # if no data is expected return raw data (usually None)
        if not model:
            return data

        # if data is a list, parse each entry
        if isinstance(data, list):
            objects = []
            for obj in data:
                objects.append(model.model_validate(obj))
        else:
            # Handle the case when data is not a list
            objects = model.model_validate(data)

        return objects