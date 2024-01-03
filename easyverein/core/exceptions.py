"""
This module contains exceptions used by the library.
"""


class EasyvereinAPIException(Exception):
    """
    Exception describing an error that occurred while interacting
    with the easyVerein API
    """


class EasyvereinAPINotFoundException(EasyvereinAPIException):
    """
    Exception describing that a requested resource or endpoint has not been found
    """


class EasyvereinAPITooManyRetriesException(EasyvereinAPIException):
    """
    Exception if the API returns a 429 Too Many Requests error
    """

    retry_after = 0
