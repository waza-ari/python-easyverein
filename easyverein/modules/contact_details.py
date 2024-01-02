"""
All methods related to contact details
"""
import logging

from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin
from ..core.client import EasyvereinClient
from ..models import ContactDetails, ContactDetailsCreate, ContactDetailsUpdate


class ContactDetailsMixin(
    CRUDMixin[ContactDetails, ContactDetailsCreate, ContactDetailsUpdate],
    RecycleBinMixin[ContactDetails],
):
    """
    All methods related to contact details
    """

    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "contact-details"
        self.return_type = ContactDetails
        self.c = client
        self.logger = logger
