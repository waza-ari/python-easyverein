"""
Main EasyVerein API class
"""
import logging

from .core.client import EasyvereinClient
from .modules.invoice import InvoiceMixin


class EasyvereinAPI(InvoiceMixin):
    """
    Main EasyVerein API class
    """

    def __init__(
        self,
        api_key,
        api_version="v1.6",
        base_url: str = "https://easyverein.com/api/",
        logger: logging.Logger = None,
    ):
        """
        Constructor setting API key and logger
        """

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("easyverein")

        self.c = EasyvereinClient(api_key, api_version, base_url, self.logger)
