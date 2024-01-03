"""
All methods related to contact details
"""
import logging

from ..core.client import EasyvereinClient
from ..models import ContactDetails, ContactDetailsCreate, ContactDetailsUpdate
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class ContactDetailsMixin(
    CRUDMixin[ContactDetails, ContactDetailsCreate, ContactDetailsUpdate],
    RecycleBinMixin[ContactDetails],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "contact-details"
        self.return_type = ContactDetails
        self.c = client
        self.logger = logger
