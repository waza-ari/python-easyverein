"""
Main EasyVerein API class
"""

import logging
from typing import Callable, cast

from .core.api_version import DEFAULT_API_VERSION, REMOVED_API_VERSIONS, SUPPORTED_API_VERSIONS
from .core.client import EasyvereinClient
from .core.responses import BearerToken
from .modules.billing_account import BillingAccountMixin
from .modules.booking import BookingMixin
from .modules.booking_project import BookingProjectMixin
from .modules.contact_details import ContactDetailsMixin
from .modules.contact_details_group import ContactDetailsGroupMixin
from .modules.custom_field import CustomFieldMixin
from .modules.invoice import InvoiceMixin
from .modules.invoice_item import InvoiceItemMixin
from .modules.member import MemberMixin
from .modules.member_group import MemberGroupMixin
from .modules.mixins.helper import parse_models


class EasyvereinAPI:
    def __init__(
        self,
        api_key,
        api_version: str = DEFAULT_API_VERSION,
        base_url: str = "https://easyverein.com/api/",
        logger: logging.Logger | None = None,
        auto_retry=False,
        token_refresh_callback: Callable[[BearerToken], None] | Callable[[], None] | None = None,
        auto_refresh_token: bool = False,
    ):
        """
        Creates the API client.

        Args:
            api_key: API token of the organization
            api_version: EasyVerein API version to use, either `v2.0` (default) or `v3.0`. The models and
                methods of this library are identical for both versions, see the usage documentation for details.
            base_url: Base URL of the API
            logger: Logger to use, defaults to a logger named `easyverein`
            auto_retry: Whether to automatically wait and retry when hitting the rate limit
            token_refresh_callback: Callback invoked when the API indicates that the token should be refreshed
            auto_refresh_token: Whether to automatically refresh the token and pass it to the callback
        """

        super().__init__()

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("easyverein")

        # Check parameters
        if api_version in REMOVED_API_VERSIONS:
            self.logger.error(REMOVED_API_VERSIONS[api_version])
            raise ValueError(REMOVED_API_VERSIONS[api_version])

        if api_version not in SUPPORTED_API_VERSIONS:
            self.logger.error(
                f"API version {api_version} is not supported. Supported versions are {SUPPORTED_API_VERSIONS}"
            )
            raise ValueError(
                f"API version {api_version} is not supported. Supported versions are {SUPPORTED_API_VERSIONS}"
            )

        self.token_refresh_callback = token_refresh_callback
        self.auto_refresh_token = auto_refresh_token
        self.c = EasyvereinClient(api_key, api_version, base_url, self.logger, self, auto_retry)

        # Add methods
        self.booking = BookingMixin(self.c, self.logger)
        self.booking_project = BookingProjectMixin(self.c, self.logger)
        self.billing_account = BillingAccountMixin(self.c, self.logger)
        self.contact_details = ContactDetailsMixin(self.c, self.logger)
        self.contact_details_group = ContactDetailsGroupMixin(self.c, self.logger)
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
        Refreshes the bearer token and makes the client use the new token.
        """

        response = self.c.fetch_one(self.c.get_url("/refresh-token"))
        token = parse_models(response.result, BearerToken)
        if not token:
            self.logger.error(f"Error refreshing token: {response.result}")
            raise ValueError(f"Error refreshing token: {response.result}")

        # update client instance to use the new token
        token = cast(BearerToken, token)
        self.c.api_key = token.Bearer
        return token
