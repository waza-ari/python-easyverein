"""
Main EasyVerein API class
"""

import logging
from typing import Callable, cast

from .core.client import EasyvereinClient
from .core.responses import BearerToken
from .modules.contact_details import ContactDetailsMixin
from .modules.custom_field import CustomFieldMixin
from .modules.invoice import InvoiceMixin
from .modules.invoice_item import InvoiceItemMixin
from .modules.member import MemberMixin
from .modules.member_group import MemberGroupMixin
from .modules.mixins.helper import parse_models

SUPPORTED_API_VERSIONS = ["v1.6", "v1.7", "v2.0"]


class EasyvereinAPI:
    def __init__(
        self,
        api_key,
        api_version="v1.7",
        base_url: str = "https://hexa.easyverein.com/api/",
        logger: logging.Logger | None = None,
        auto_retry=False,
        token_refresh_callback: Callable[[BearerToken], None] | Callable[[], None] | None = None,
        auto_refresh_token: bool = False,
    ):
        """
        Constructor setting API key and logger. Test
        """

        super().__init__()

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("easyverein")

        # Check parameters
        if api_version not in SUPPORTED_API_VERSIONS:
            self.logger.error(
                f"API version {api_version} is not supported. Supported versions are {SUPPORTED_API_VERSIONS}"
            )
            raise ValueError(
                f"API version {api_version} is not supported. Supported versions are {SUPPORTED_API_VERSIONS}"
            )

        if (auto_refresh_token or token_refresh_callback) and api_version != "v2.0":
            raise ValueError("Token refresh is only supported in API version v2.0")

        self.token_refresh_callback = token_refresh_callback
        self.auto_refresh_token = auto_refresh_token
        self.c = EasyvereinClient(api_key, api_version, base_url, self.logger, self, auto_retry)

        # Add methods
        self.contact_details = ContactDetailsMixin(self.c, self.logger)
        self.custom_field = CustomFieldMixin(self.c, self.logger)
        self.invoice = InvoiceMixin(self.c, self.logger)
        self.invoice_item = InvoiceItemMixin(self.c, self.logger)
        self.member = MemberMixin(self.c, self.logger)
        self.member_group = MemberGroupMixin(self.c, self.logger)

    def handle_token_refresh(self):
        """
        This method is called by the client if a token refresh is required according to the API response.
        """

        if self.token_refresh_callback:
            self.logger.info("Notifying token refresh callback to refresh token")
            self.token_refresh_callback(self.refresh_token() if self.auto_refresh_token else None)

    def refresh_token(self) -> BearerToken:
        """
        Refreshes the bearer token (only valid for API v2.0)
        """

        if not self.c.api_version == "v2.0":
            self.logger.error("Refresh token is only available for API v2.0")
            raise ValueError("Refresh token is only available for API v2.0")

        response = self.c.fetch_one(self.c.get_url("/refresh-token"))
        token = parse_models(response.result, BearerToken)
        if not token:
            self.logger.error(f"Error refreshing token: {response.result}")
            raise ValueError(f"Error refreshing token: {response.result}")

        return cast(BearerToken, token)
