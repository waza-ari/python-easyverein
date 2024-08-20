"""
Main EasyVerein API class
"""

from __future__ import annotations

import logging
from io import BufferedReader
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING, Any

import requests
from pydantic import BaseModel
from requests.structures import CaseInsensitiveDict

from .exceptions import (
    EasyvereinAPIException,
    EasyvereinAPINotFoundException,
    EasyvereinAPITooManyRetriesException,
)
from .responses import ResponseSchema

if TYPE_CHECKING:
    from .. import EasyvereinAPI


class EasyvereinClient:
    """
    Class encapsulating common function used by all API methods
    """

    def __init__(
        self,
        api_key,
        api_version,
        base_url,
        logger: logging.Logger,
        instance: EasyvereinAPI,
        auto_retry=False,
    ):
        """
        Constructor setting API key and logger
        """
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version
        self.logger = logger
        self.api_instance = instance
        self.auto_retry = auto_retry

    def _get_header(self):
        """
        Constructs a header for the API request
        """
        return {"Authorization": "Bearer " + self.api_key}

    def get_url(self, path: str, url_params: dict | None = None) -> str:
        """
        Constructs a URL for the API request.

        :param path: Base path of the request
        :param url_params: additional path parameters to append
        """
        url = f"{self.base_url}{self.api_version}{path}"

        self.logger.debug(f"Base URL is {url}")

        if url_params:
            for key, value in url_params.items():
                if not value:
                    continue
                self.logger.debug(f"Adding {key}={value} path parameter to URL")
                if "?" not in url:
                    url += f"?{key}={value}"
                else:
                    url += f"&{key}={value}"

        self.logger.debug(f"Final constructed URL is {url}")

        return url

    def _do_request(  # noqa: PLR0913
        self,
        method: str,
        url: str,
        binary: bool = False,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        files: dict[str, BufferedReader] | None = None,
    ) -> tuple[int, dict[str, Any] | requests.Response | None]:
        """
        Helper method that performs an actual call against the API, catching the most common errors
        """
        self.logger.debug("Performing %s request to %s", method, url)
        if data:
            self.logger.debug("Request data: %s", data)
        if headers:
            self.logger.debug("Provided request headers: %s", headers)

        # Merge auth header with custom headers
        final_headers = self._get_header() | (headers or {})

        self.logger.debug("Final request headers: %s", final_headers)

        func = getattr(requests, method)
        res: requests.Response
        if data:
            res = func(url, headers=final_headers, json=data, files=files or {})
        else:
            res = func(url, headers=final_headers, files=files)

        self.logger.debug("Request returned status code %d", res.status_code)

        if res.status_code == 429:
            retry_after = res.headers["Retry-After"]

            try:
                retry_after = int(retry_after)
            except ValueError:
                self.logger.error("Unable to parse Retry-After header while handling 429 response code.")
                self.logger.debug("Retry-After header: %s", retry_after)
                retry_after = 0

            self.logger.warning(
                "Request returned status code 429, too many requests. Wait %d seconds",
                retry_after,
            )
            if self.auto_retry:
                self.logger.warning("Retrying after %d seconds sleep.", retry_after)
                sleep(retry_after)
                if files:
                    for v in files.values():
                        v.seek(0)  # reset file seek, as it has been moved by the previous call

                return self._do_request(method, url, binary, data, headers, files)
            else:
                raise EasyvereinAPITooManyRetriesException(
                    f"Too many requests, please wait {retry_after} seconds and try again.",
                    retry_after=retry_after,
                )

        # If API version is v2.0, check if token refresh is required
        if self.api_version == "v2.0" and res.headers.get("tokenRefreshNeeded", "false") == "True":
            self.logger.info("Token refresh required")
            self.api_instance.handle_token_refresh()

        if res.status_code == 404:
            self.logger.warning("Request returned status code 404, resource not found")
            raise EasyvereinAPINotFoundException("Requested resource not found")

        # In some cases (for example on 204 delete) the response is empty
        if res.content == b"":
            return res.status_code, None

        # If content is supposed to be binary, return the entire response to maintain headers
        if binary:
            return res.status_code, res

        # Try to parse response as JSON and return it for further processing
        try:
            content = res.json()
        except ValueError:
            self.logger.error("Unable to parse response content as JSON")
            self.logger.debug("Response content: %s", res.content)
            content = None

        return res.status_code, content

    def create(
        self,
        url,
        data: BaseModel,
        status_code: int = 201,
    ) -> ResponseSchema:
        """
        Method to create an object in the API
        """
        return self._handle_response(
            self._do_request(
                "post",
                url,
                data=data.model_dump(exclude_none=True, exclude_unset=True, by_alias=True),
            ),
            status_code,
        )

    def delete(self, url, status_code: int = 204):
        """
        Method to delete an object in the API
        """
        return self._handle_response(self._do_request("delete", url), expected_status_code=status_code)

    def update(self, url, data: BaseModel, status_code: int = 200) -> ResponseSchema:
        """
        Method to update an object in the API
        """
        return self._handle_response(
            self._do_request(
                "patch",
                url,
                data=data.model_dump(exclude_none=True, exclude_unset=True, by_alias=True),
            ),
            expected_status_code=status_code,
        )

    def upload(
        self,
        url: str,
        field_name: str,
        file: Path,
        status_code: int = 200,
    ) -> ResponseSchema:
        """
        This method uploads a file to a certain endpoint.

        Only tested with invoices so far
        """
        # Check that path is a file and it exists
        if not file.exists() or not file.is_file():
            self.logger.error("File does not exist or is not a file.")
            raise FileNotFoundError("File does not exist")

        files = {field_name: open(file, "rb")}
        headers = {"Content-Disposition": f'name="file"; filename="{file.name}"'}

        return self._handle_response(
            self._do_request(
                "patch",
                url,
                headers=headers,
                files=files,
            ),
            status_code,
        )

    def fetch(self, url) -> ResponseSchema:
        """
        Helper method that fetches a result from an API call

        Only supports GET endpoints
        """
        res = self._do_request("get", url)
        return self._handle_response(res, 200)

    def fetch_file(self, url: str) -> tuple[bytes, CaseInsensitiveDict[str]]:
        """
        Helper method that fetches a file from the API including the authentication header

        Returns the raw bytes object and the entire header for further processing
        """
        status_code, res = self._do_request("get", url, binary=True)

        # Response needs to be a Response object
        if not isinstance(res, requests.Response):
            self.logger.error("Request to download file failed with unexpected response")
            raise EasyvereinAPIException("Request to download file failed with unexpected response")

        # Check if status code is 200
        if status_code != 200:
            self.logger.error(f"Request to download file failed with unexpected status code {status_code}")
            raise EasyvereinAPIException(f"Request to download file failed with unexpected status code {status_code}")

        return res.content, res.headers

    def fetch_one(self, url) -> ResponseSchema:
        """
        Helper method that fetches a result from an API call

        Only supports GET endpoints
        """
        reply = self.fetch(url)
        if isinstance(reply.result, list):
            if len(reply.result) == 0:
                reply.result = None
                reply.count = 0
                return reply

            self.logger.warning("One object was requested, but multiple objects were returned. Returning first.")
            self.logger.debug(f"In total {len(reply.result)} objects where returned.")
            reply.result = reply.result[0]
            reply.count = 1
            return reply

        return reply

    def fetch_paginated(self, url, limit=100) -> ResponseSchema:
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

            if not isinstance(result, dict):
                self.logger.error("Could not fetch paginated API %s, status code %d", url, status_code)
                self.logger.debug("API response: %s", result)
                raise EasyvereinAPIException(
                    f"Could not fetch paginated API {url}, " f"status code {status_code}. API response: {result}"
                )

            if not status_code == 200:
                self.logger.error("Could not fetch paginated API %s, status code %d", url, status_code)
                self.logger.debug("API response: %s", result)
                raise EasyvereinAPIException(
                    f"Could not fetch paginated API {url}, " f"status code {status_code}. API response: {result}"
                )

            resources.extend(result["results"])
            url = result["next"]

        return self._handle_response((status_code, resources), 200)

    def _handle_response(
        self,
        res: tuple[int, dict[str, Any] | list[dict[str, Any]] | requests.Response | None],
        expected_status_code=200,
    ) -> ResponseSchema:
        """
        Helper method that handles API responses
        """
        status_code, data = res
        if status_code != expected_status_code:
            raise EasyvereinAPIException(f"API returned status code {status_code}. API response: {data}")
        else:
            self.logger.debug("API returned status code %d", status_code)

        self.logger.debug("Received raw data: %s", data)

        if data is None:
            return ResponseSchema(result=None, count=0, response_code=status_code)

        # if data is a list, parse each entry
        # fetch_paginated returns a list of result entries instead of raw data, this is why this case is here.
        if isinstance(data, list):
            return ResponseSchema(
                result=data,
                count=len(data),
                response_code=status_code,
            )
        elif isinstance(data, dict) and "results" in data:
            return ResponseSchema(
                result=data["results"],
                count=data.get("count", 0),
                response_code=status_code,
            )
        elif isinstance(data, requests.Response):
            # Return the raw response object
            return ResponseSchema(
                result=None,
                count=0,
                response_code=status_code,
                response=data,
            )
        else:
            # Return the single object
            return ResponseSchema(
                result=data,
                count=1,
                response_code=status_code,
            )
