"""
Main EasyVerein API class
"""
import logging

from .core.client import EasyvereinClient
from .modules.invoice import InvoiceMixin


class EasyvereinAPI(InvoiceMixin):
    """
    API Client to work wth the EasyVerein API. All methods
    are available directly as methods of this class

    Usage:

    ```python
    from easyverein import EasyvereinAPI
    api = EasyvereinAPI(api_key="your_api_key")
    invoices = api.get_invoices()
    ```
    """

    def __init__(
        self,
        api_key,
        api_version="v1.6",
        base_url: str = "https://easyverein.com/api/",
        logger: logging.Logger = None,
    ):
        """
        Constructor setting API key and logger. Test
        """

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("easyverein")

        self.c = EasyvereinClient(api_key, api_version, base_url, self.logger)
