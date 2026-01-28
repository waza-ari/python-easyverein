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

    def __init__(self, message, retry_after: int = 0):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        self.retry_after = retry_after

    retry_after = 0
