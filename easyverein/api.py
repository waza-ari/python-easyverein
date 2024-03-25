"""
Main EasyVerein API class
"""

import logging

from .core.client import EasyvereinClient
from .modules.contact_details import ContactDetailsMixin
from .modules.custom_field import CustomFieldMixin
from .modules.invoice import InvoiceMixin
from .modules.invoice_item import InvoiceItemMixin
from .modules.member import MemberMixin
from .modules.member_custom_field import MemberCustomFieldMixin


class EasyvereinAPI:
    def __init__(
        self,
        api_key,
        api_version="v1.7",
        base_url: str = "https://hexa.easyverein.com/api/",
        logger: logging.Logger = None,
    ):
        """
        Constructor setting API key and logger. Test
        """

        super().__init__()

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("easyverein")

        self.c = EasyvereinClient(api_key, api_version, base_url, self.logger, self)

        # Add methods

        self.contact_details = ContactDetailsMixin(self.c, self.logger)
        self.custom_field = CustomFieldMixin(self.c, self.logger)
        self.invoice = InvoiceMixin(self.c, self.logger)
        self.invoice_item = InvoiceItemMixin(self.c, self.logger)
        self.member = MemberMixin(self.c, self.logger)
        self.member_custom_field = MemberCustomFieldMixin(self.c, self.logger)
